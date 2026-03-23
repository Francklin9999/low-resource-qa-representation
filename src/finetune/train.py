"""
QLoRA fine-tuning on translated QA data.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from trl import SFTTrainer, SFTConfig

from paths import DATA_DIR, TRAINING_DIR, FINETUNE_CONFIG
from utils import load_config, load_jsonl
from utils.prompts import FINETUNE_SYSTEM_PROMPT
from src.finetune.gpu import free_gpu_memory


logger = logging.getLogger("mqab.finetune.train")

_FINETUNE_CFG = load_config(FINETUNE_CONFIG)
_DEFAULT_CFG = _FINETUNE_CFG.get("training", {})


@dataclass
class TrainConfig:
    """Configuration for QLoRA fine-tuning, loaded from configs/finetune.yaml."""

    base_model: str = _DEFAULT_CFG.get("base_model")
    output_dir: str = ""

    # LoRA
    lora_r: int = _DEFAULT_CFG.get("lora_r")
    lora_alpha: int = _DEFAULT_CFG.get("lora_alpha")
    lora_dropout: float = _DEFAULT_CFG.get("lora_dropout")
    lora_target_modules: list[str] = field(
        default_factory=lambda: _DEFAULT_CFG.get("lora_target_modules")
    )

    # Training hyperparameters
    learning_rate: float = float(_DEFAULT_CFG.get("learning_rate", 0))
    epochs: int = _DEFAULT_CFG.get("epochs")
    per_device_train_batch_size: int = _DEFAULT_CFG.get("per_device_train_batch_size")
    per_device_eval_batch_size: int = _DEFAULT_CFG.get("per_device_eval_batch_size")
    gradient_accumulation_steps: int = _DEFAULT_CFG.get("gradient_accumulation_steps")
    max_length: int = _DEFAULT_CFG.get("max_length")
    warmup_steps: int = _DEFAULT_CFG.get("warmup_steps")
    weight_decay: float = _DEFAULT_CFG.get("weight_decay")
    lr_scheduler_type: str = _DEFAULT_CFG.get("lr_scheduler_type")

    # Language (from top-level finetune.yaml `language` field)
    lang: str = _FINETUNE_CFG.get("language")

    # Data paths (auto-set from lang if not overridden)
    train_data: str = ""
    val_data: str = ""

    def __post_init__(self):
        missing = []
        for fld in ("base_model", "lang", "lora_r", "lora_alpha", "lora_dropout",
                     "lora_target_modules", "epochs", "per_device_train_batch_size",
                     "per_device_eval_batch_size", "gradient_accumulation_steps",
                     "max_length", "lr_scheduler_type"):
            if getattr(self, fld) is None:
                missing.append(fld)
        if missing:
            raise ValueError(
                f"Missing required training config fields in configs/finetune.yaml:\n"
                + "\n".join(f"  - training.{m}" for m in missing)
            )
        if not self.train_data:
            self.train_data = str(TRAINING_DIR / self.lang / "train.jsonl")
        if not self.val_data:
            self.val_data = str(TRAINING_DIR / self.lang / "val.jsonl")
        if not self.output_dir:
            self.output_dir = str(TRAINING_DIR / "checkpoints" / self.lang)

    # Misc
    seed: int = _DEFAULT_CFG.get("seed")
    logging_steps: int = _DEFAULT_CFG.get("logging_steps")
    eval_steps: int = _DEFAULT_CFG.get("eval_steps")
    save_steps: int = _DEFAULT_CFG.get("save_steps")
    save_total_limit: int = _DEFAULT_CFG.get("save_total_limit")
    bf16: bool = _DEFAULT_CFG.get("bf16")


def format_chat(sample: dict, tokenizer: AutoTokenizer) -> str:
    """Format a sample into chat template for training."""
    messages = [
        {"role": "system", "content": FINETUNE_SYSTEM_PROMPT},
        {"role": "user", "content": sample["prompt"]},
        {"role": "assistant", "content": sample["target"]},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False)


def load_model_and_tokenizer(config: TrainConfig):
    """Load the base model in 4-bit quantization and apply LoRA."""
    logger.info("Loading base model: %s", config.base_model)

    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        config.base_model,
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )

    model = prepare_model_for_kbit_training(model)

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.lora_target_modules,
        bias="none",
    )

    model = get_peft_model(model, lora_config)

    trainable, total = model.get_nb_trainable_parameters()
    logger.info(
        "Model loaded. Trainable: %s / %s (%.2f%%)",
        f"{trainable:,}", f"{total:,}", 100 * trainable / total,
    )

    return model, tokenizer


def train(config: TrainConfig | None = None) -> Path:
    """Run QLoRA fine-tuning.

    Returns path to the saved adapter checkpoint.
    """
    if config is None:
        config = TrainConfig()

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    free_gpu_memory()

    # Load model
    model, tokenizer = load_model_and_tokenizer(config)

    # Load data
    logger.info("Loading training data from %s", config.train_data)
    train_raw = load_jsonl(config.train_data)
    val_raw = load_jsonl(config.val_data)

    # Format as chat conversations
    train_texts = [format_chat(s, tokenizer) for s in train_raw]
    val_texts = [format_chat(s, tokenizer) for s in val_raw]

    train_dataset = Dataset.from_dict({"text": train_texts})
    val_dataset = Dataset.from_dict({"text": val_texts})

    logger.info("Train: %d samples, Val: %d samples", len(train_dataset), len(val_dataset))

    # Training arguments
    sft_config = SFTConfig(
        output_dir=str(output_dir),
        num_train_epochs=config.epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        lr_scheduler_type=config.lr_scheduler_type,
        warmup_steps=config.warmup_steps,
        weight_decay=config.weight_decay,
        bf16=config.bf16,
        logging_steps=config.logging_steps,
        eval_strategy="steps",
        eval_steps=config.eval_steps,
        save_strategy="steps",
        save_steps=config.save_steps,
        save_total_limit=config.save_total_limit,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        max_length=config.max_length,
        dataset_text_field="text",
        seed=config.seed,
        gradient_checkpointing=True,
        report_to="none",
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=sft_config,
    )

    logger.info("Starting training for %d epochs...", config.epochs)
    trainer.train()

    # Save adapter
    adapter_path = output_dir / "final_adapter"
    model.save_pretrained(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))
    logger.info("Adapter saved -> %s", adapter_path)

    # Save training config
    config_path = output_dir / "train_config.json"
    with open(config_path, "w") as f:
        json.dump({
            "base_model": config.base_model,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
            "epochs": config.epochs,
            "learning_rate": config.learning_rate,
            "max_length": config.max_length,
            "train_samples": len(train_dataset),
            "val_samples": len(val_dataset),
        }, f, indent=2)

    return adapter_path
