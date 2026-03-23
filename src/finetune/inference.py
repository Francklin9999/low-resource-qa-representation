"""
Inference with the fine-tuned QLoRA model.

Supports three modes:
1. Direct baseline - ask the model in the target language directly
2. Translate-pivot baseline - translate to English, ask base model, translate back
3. Fine-tuned pipeline - translate to English, ask fine-tuned model, translate back
"""

import logging
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from paths import TRAINING_DIR
from src.finetune.dataset import format_prompt
from src.translate import translate
from utils.prompts import FINETUNE_SYSTEM_PROMPT

logger = logging.getLogger("mqab.finetune.inference")


def load_finetuned_model(
    base_model: str,
    adapter_path: str | Path | None = None,
) -> tuple:
    """Load base model + LoRA adapter for inference.

    Returns (model, tokenizer).
    """
    if adapter_path is None:
        adapter_path = TRAINING_DIR / "checkpoints" / "final_adapter"
    adapter_path = Path(adapter_path)

    logger.info("Loading base model: %s", base_model)
    logger.info("Loading adapter from: %s", adapter_path)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        str(adapter_path),
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )

    model = PeftModel.from_pretrained(model, str(adapter_path))
    model.eval()

    logger.info("Fine-tuned model loaded and ready for inference.")
    return model, tokenizer


def predict(
    model,
    tokenizer,
    context: str,
    question: str,
    max_new_tokens: int = 128,
) -> str:
    """Generate an answer given context and question using the fine-tuned model."""
    prompt = format_prompt(context=context, question=question)

    messages = [
        {"role": "system", "content": FINETUNE_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
        )

    # Decode only the generated part (skip the prompt)
    generated = outputs[0][inputs["input_ids"].shape[1]:]
    answer = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return answer


def run_finetuned_pipeline(
    test_data: list[dict],
    model,
    tokenizer,
    lang: str,
) -> list[dict]:
    """Run the full fine-tuned translate-pivot pipeline on test data.

    For each sample:
    1. Use pre-translated English context and question (from prepare step)
    2. Run through fine-tuned model -> English answer
    3. Translate English answer back to source language

    Returns list of predictions with all intermediate results.
    """
    predictions = []

    for i, sample in enumerate(test_data):
        context_en = sample.get("context_en", "")
        question_en = sample.get("question_en", "")

        # If not pre-translated, translate now
        if not context_en:
            context_en = translate(sample["context"], src_lang=lang, tgt_lang="en")
        if not question_en:
            question_en = translate(sample["question"], src_lang=lang, tgt_lang="en")

        # Get English answer from fine-tuned model
        answer_en = predict(model, tokenizer, context=context_en, question=question_en)

        # Translate answer back to source language
        answer_src = translate(answer_en, src_lang="en", tgt_lang=lang)

        predictions.append({
            "id": sample.get("id", f"test_{i:05d}"),
            "question_src": sample["question"],
            "context_src": sample.get("context", ""),
            "gold_src": sample.get("answer", ""),
            "context_en": context_en,
            "question_en": question_en,
            "answer_en": answer_en,
            "answer_src": answer_src,
        })

        if (i + 1) % 10 == 0:
            logger.info("  Predicted %d / %d", i + 1, len(test_data))

    logger.info("Fine-tuned pipeline complete: %d predictions", len(predictions))
    return predictions


def run_base_model_pipeline(
    test_data: list[dict],
    model,
    tokenizer,
    lang: str,
) -> list[dict]:
    """Run translate-pivot with the BASE model (no fine-tuning) for baseline comparison.

    Same pipeline as run_finetuned_pipeline but uses the base model without adapter.
    Useful when the model is loaded without merging the adapter.
    """
    # Disable adapter for base model baseline
    if hasattr(model, "disable_adapter_layers"):
        model.disable_adapter_layers()

    predictions = run_finetuned_pipeline(test_data, model, tokenizer, lang=lang)

    # Re-enable adapter
    if hasattr(model, "enable_adapter_layers"):
        model.enable_adapter_layers()

    # Tag predictions
    for p in predictions:
        p["pipeline"] = "base_translate_pivot"

    return predictions
