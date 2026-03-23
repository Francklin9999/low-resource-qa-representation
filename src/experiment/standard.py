"""Standard experiment: direct vs translate-pivot pipelines."""

from pathlib import Path

from src.llm import get_provider
from src.translate import translate
from src.evaluate import semantic_similarity

from .common import (
    LANGUAGES, SYSTEM_PROMPT, DATA_DIR,
    load_data, save_results, log_summary, logger,
)


def run_experiment(
    provider_name: str,
    model: str,
    run_dir: Path,
    lang: str,
    max_samples: int | None = None,
):
    """Run both pipelines for a given provider/model and save results."""
    lang_info = LANGUAGES[lang]
    lang_name = lang_info["name"]
    pivot = lang_info.get("pivot", "en")

    data_path = DATA_DIR / "processed" / f"{lang_name}_filtered.json"
    questions = load_data(data_path, max_samples)

    logger.info("=" * 60)
    logger.info("Experiment: %s/%s | lang=%s | pivot=%s | n=%d", provider_name, model, lang, pivot, len(questions))
    logger.info("=" * 60)

    llm = get_provider(provider_name, model)
    results = []

    for i, item in enumerate(questions):
        question = item["question"]
        gold = item["answer"]
        translated_question = item.get("translated_question", "")

        # Pipeline 1: Direct - ask in source language
        direct_response = llm.ask(question, system_prompt=SYSTEM_PROMPT)
        direct_response_pivot = translate(direct_response, src_lang=lang, tgt_lang=pivot)
        direct_sim = semantic_similarity(direct_response, gold)

        # Pipeline 2: Translate - translate to pivot language, ask, translate back
        question_pivot = translate(question, src_lang=lang, tgt_lang=pivot)
        response_pivot = llm.ask(question_pivot, system_prompt=SYSTEM_PROMPT)
        translate_response = translate(response_pivot, src_lang=pivot, tgt_lang=lang)
        translate_sim = semantic_similarity(translate_response, gold)

        results.append({
            "question": question,
            "translated_question": translated_question,
            "gold": gold,
            "pivot": pivot,
            "direct_response": direct_response,
            "direct_response_pivot": direct_response_pivot,
            "direct_semantic_similarity": round(direct_sim, 4),
            "translate_response": translate_response,
            "translate_response_pivot": response_pivot,
            "translate_semantic_similarity": round(translate_sim, 4),
        })

        logger.info(
            "  [%d/%d] direct_sim=%.2f  translate_sim=%.2f",
            i + 1, len(questions), direct_sim, translate_sim,
        )

    safe_model = model.replace("/", "_")
    output_path = run_dir / f"{provider_name}_{safe_model}_{lang}.json"
    save_results(results, output_path)
    log_summary(results, {
        "Direct avg sim": "direct_semantic_similarity",
        "Translate avg sim": "translate_semantic_similarity",
    }, output_path)

    return results
