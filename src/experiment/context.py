"""Context experiment: direct vs translate-pivot with gold passages."""

from pathlib import Path

from src.llm import get_provider
from src.translate import translate
from src.evaluate import semantic_similarity, exact_match, f1_score

from .common import (
    CONTEXT_SYSTEM_PROMPT, DATA_DIR,
    load_data, save_results, log_summary, logger,
)


def run_context_experiment(
    provider_name: str,
    model: str,
    run_dir: Path,
    lang: str,
    max_samples: int | None = None,
):
    """Run an API model with context on the same test split used for fine-tuning.

    Pipelines:
    1. Direct - send context + question in source language to the LLM
    2. Translate-pivot - translate context + question to English, ask LLM, translate back
    """
    test_path = DATA_DIR / "training" / "splits" / f"{lang}_test.json"
    test_data = load_data(test_path, max_samples)

    logger.info("=" * 60)
    logger.info("Context experiment: %s/%s | lang=%s | n=%d", provider_name, model, lang, len(test_data))
    logger.info("=" * 60)

    llm = get_provider(provider_name, model)
    results = []

    for i, item in enumerate(test_data):
        question = item["question"]
        context = item.get("context", "")
        gold = item["answer"]
        context_en = item.get("context_en", "")
        question_en = item.get("question_en", "")

        # Translate if not pre-translated
        if not context_en:
            context_en = translate(context, src_lang=lang, tgt_lang="en")
        if not question_en:
            question_en = translate(question, src_lang=lang, tgt_lang="en")

        gold_en = item.get("answer_en", "")

        # Pipeline 1: Direct - source language context + question
        direct_prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"
        direct_response = llm.ask(direct_prompt, system_prompt=CONTEXT_SYSTEM_PROMPT)
        direct_sim = semantic_similarity(direct_response, gold)

        # Pipeline 2: Translate-pivot - English context + question -> English answer -> source lang
        translate_prompt = f"Context:\n{context_en}\n\nQuestion:\n{question_en}\n\nAnswer:\n"
        response_en = llm.ask(translate_prompt, system_prompt=CONTEXT_SYSTEM_PROMPT)
        response_src = translate(response_en, src_lang="en", tgt_lang=lang)
        translate_sim = semantic_similarity(response_src, gold)

        results.append({
            "id": item.get("id", i),
            f"question_{lang}": question,
            f"gold_{lang}": gold,
            "gold_en": gold_en,
            # Direct
            "direct_response": direct_response,
            "direct_sim": round(direct_sim, 4),
            "direct_em": exact_match(direct_response, gold),
            "direct_f1": round(f1_score(direct_response, gold), 4),
            # Translate-pivot
            "translate_response_en": response_en,
            f"translate_response_{lang}": response_src,
            "translate_sim": round(translate_sim, 4),
            "translate_em": exact_match(response_src, gold),
            "translate_f1": round(f1_score(response_src, gold), 4),
            # English-side metrics
            "translate_sim_en": round(semantic_similarity(response_en, gold_en), 4) if gold_en else None,
            "translate_em_en": exact_match(response_en, gold_en) if gold_en else None,
            "translate_f1_en": round(f1_score(response_en, gold_en), 4) if gold_en else None,
        })

        logger.info(
            "  [%d/%d] direct_sim=%.2f  translate_sim=%.2f",
            i + 1, len(test_data), direct_sim, translate_sim,
        )

    safe_model = model.replace("/", "_")
    output_path = run_dir / f"context_{provider_name}_{safe_model}_{lang}.json"
    save_results(results, output_path)
    log_summary(results, {
        "Direct avg sim": "direct_sim",
        "Translate avg sim": "translate_sim",
        "Translate avg sim (EN-side)": "translate_sim_en",
    }, output_path)

    return results
