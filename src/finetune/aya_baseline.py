"""
Aya-23-8B baseline for comparison against the fine-tuned pipeline.

Runs two modes:
1. Direct: Aya answers directly in the source language (it supports African languages)
2. Translate-pivot: Same pipeline as Fine-tuned model (translate to English, ask Aya, translate back)
"""

import logging

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from src.finetune.dataset import format_prompt
from src.finetune.gpu import free_gpu_memory
from src.translate import translate
from utils.prompts import FINETUNE_SYSTEM_PROMPT

logger = logging.getLogger("mqab.finetune.aya")

AYA_MODEL = "CohereForAI/aya-23-8B"


def load_aya_model() -> tuple:
    """Load Aya-23-8B in 4-bit quantization."""
    logger.info("Loading Aya-23-8B in 4-bit quantization...")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(AYA_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        AYA_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )
    model.eval()

    logger.info("Aya-23-8B loaded.")
    return model, tokenizer


def unload_aya_model(model, tokenizer):
    """Unload Aya model and free GPU memory."""
    del model
    del tokenizer
    free_gpu_memory()
    logger.info("Aya model unloaded.")


def aya_predict(
    model,
    tokenizer,
    context: str,
    question: str,
    max_new_tokens: int = 128,
) -> str:
    """Generate answer using Aya-23-8B with the same prompt format."""
    prompt = format_prompt(context=context, question=question)

    messages = [
        {"role": "system", "content": FINETUNE_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
        )

    generated = outputs[0][inputs["input_ids"].shape[1] :]
    answer = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return answer


def aya_predict_direct(
    model,
    tokenizer,
    context: str,
    question: str,
    lang: str,
    max_new_tokens: int = 128,
) -> str:
    """Ask Aya directly in the source language (no translation)."""
    prompt = (
        f"Answer the question using only the context. "
        f"Answer in {lang}. Be concise, give only the answer.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:\n"
    )

    messages = [
        {"role": "user", "content": prompt},
    ]

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
        )

    generated = outputs[0][inputs["input_ids"].shape[1] :]
    answer = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return answer


def run_aya_baseline(
    test_data: list[dict],
    lang: str,
) -> dict:
    """Run Aya-23-8B baselines: direct + translate-pivot.

    Returns dict with 'direct' and 'translate_pivot' prediction lists.
    """
    model, tokenizer = load_aya_model()

    lang_names = {
        "fon": "Fon",
        "hau": "Hausa",
        "yor": "Yoruba",
        "ibo": "Igbo",
        "swa": "Swahili",
        "kin": "Kinyarwanda",
        "twi": "Twi",
        "wol": "Wolof",
        "zul": "Zulu",
        "bem": "Bemba",
    }
    lang_name = lang_names.get(lang, lang)

    direct_preds = []
    translate_preds = []

    for i, sample in enumerate(test_data):
        context_src = sample.get("context", "")
        question_src = sample["question"]
        context_en = sample.get("context_en", "")
        question_en = sample.get("question_en", "")

        # If not pre-translated, translate now
        if not context_en:
            context_en = translate(context_src, src_lang=lang, tgt_lang="en")
        if not question_en:
            question_en = translate(question_src, src_lang=lang, tgt_lang="en")

        # Direct baseline: Aya answers in source language
        direct_answer = aya_predict_direct(
            model, tokenizer, context_src, question_src, lang_name
        )

        direct_preds.append({
            "id": sample.get("id", f"test_{i:05d}"),
            "answer_src": direct_answer,
        })

        # Translate-pivot: same as Fine-tuned model pipeline but with Aya
        answer_en = aya_predict(model, tokenizer, context_en, question_en)
        answer_src = translate(answer_en, src_lang="en", tgt_lang=lang)

        translate_preds.append({
            "id": sample.get("id", f"test_{i:05d}"),
            "answer_en": answer_en,
            "answer_src": answer_src,
        })

        if (i + 1) % 10 == 0:
            logger.info("  Aya predicted %d / %d", i + 1, len(test_data))

    logger.info("Aya baseline complete: %d predictions", len(test_data))

    # Unload to free GPU for next model
    unload_aya_model(model, tokenizer)

    return {
        "direct": direct_preds,
        "translate_pivot": translate_preds,
    }
