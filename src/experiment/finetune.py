"""Fine-tune experiment: base direct vs base translate-pivot vs fine-tuned translate-pivot."""

from pathlib import Path

from src.translate import translate
from src.evaluate import semantic_similarity
from src.finetune.inference import load_finetuned_model, predict

from .common import (
    LANGUAGES, DATA_DIR,
    load_data, save_results, log_summary, logger,
)


def run_finetune_experiment(
    run_dir: Path,
    lang: str,
    base_model: str,
    max_samples: int | None = None,
    adapter_path: str | None = None,
):
    """Run three-way comparison: direct (base) vs translate-pivot (base) vs translate-pivot (fine-tuned).

    Uses context-enriched data and the fine-tuned QLoRA model.
    """
    lang_info = LANGUAGES[lang]
    lang_name = lang_info["name"]

    test_path = DATA_DIR / "training" / "splits" / f"{lang_name}_test.json"
    test_data = load_data(test_path, max_samples)

    logger.info("=" * 60)
    logger.info("Finetune experiment: lang=%s | n=%d", lang, len(test_data))
    logger.info("=" * 60)

    model, tokenizer = load_finetuned_model(base_model=base_model, adapter_path=adapter_path)

    results = []
    for i, item in enumerate(test_data):
        question = item["question"]
        context = item.get("context", "")
        gold = item["answer"]
        context_en = item.get("context_en", "")
        question_en = item.get("question_en", "")

        # Translate if needed
        if not context_en:
            context_en = translate(context, src_lang=lang, tgt_lang="en")
        if not question_en:
            question_en = translate(question, src_lang=lang, tgt_lang="en")

        # Pipeline 1: Direct - base model answers in source language
        model.disable_adapter_layers()
        direct_response = predict(model, tokenizer, context="", question=question)
        direct_sim = semantic_similarity(direct_response, gold)

        # Pipeline 2: Translate-pivot with base model (no fine-tuning)
        base_response_en = predict(model, tokenizer, context=context_en, question=question_en)
        base_response_src = translate(base_response_en, src_lang="en", tgt_lang=lang)
        base_sim = semantic_similarity(base_response_src, gold)

        # Pipeline 3: Translate-pivot with fine-tuned model
        model.enable_adapter_layers()
        ft_response_en = predict(model, tokenizer, context=context_en, question=question_en)
        ft_response_src = translate(ft_response_en, src_lang="en", tgt_lang=lang)
        ft_sim = semantic_similarity(ft_response_src, gold)

        results.append({
            "question": question,
            "context": context,
            "gold": gold,
            "direct_response": direct_response,
            "direct_semantic_similarity": round(direct_sim, 4),
            "base_translate_response": base_response_src,
            "base_translate_response_en": base_response_en,
            "base_translate_semantic_similarity": round(base_sim, 4),
            "finetune_response": ft_response_src,
            "finetune_response_en": ft_response_en,
            "finetune_semantic_similarity": round(ft_sim, 4),
        })

        logger.info(
            "  [%d/%d] direct=%.2f  base_pivot=%.2f  finetune=%.2f",
            i + 1, len(test_data), direct_sim, base_sim, ft_sim,
        )

    safe_model = base_model.replace("/", "_")
    output_path = run_dir / f"finetune_{safe_model}_{lang}.json"
    save_results(results, output_path)
    log_summary(results, {
        "Direct avg sim": "direct_semantic_similarity",
        "Base translate avg sim": "base_translate_semantic_similarity",
        "Fine-tuned avg sim": "finetune_semantic_similarity",
    }, output_path)

    return results
