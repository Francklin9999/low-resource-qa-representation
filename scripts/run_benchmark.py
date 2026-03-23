"""
Benchmark API/local models on the same test splits used for fine-tuning.

Runs each model from benchmark.yaml on the finetune test data with context,
producing results directly comparable to the fine-tuned model evaluation.

Usage:
    python scripts/run_benchmark.py                          # all models, all languages with test data
    python scripts/run_benchmark.py --lang hau yor           # specific languages
    python scripts/run_benchmark.py --provider openai        # single provider
    python scripts/run_benchmark.py --max-samples 10         # limit samples (for testing)
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ensure project root is on sys.path when running as a script
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()

from src.llm import get_provider
from src.translate import translate
from src.evaluate import semantic_similarity, exact_match, f1_score
from paths import TRAINING_DIR, RESULTS_DIR, BENCHMARK_CONFIG
from utils import load_config
from utils.prompts import CONTEXT_SYSTEM_PROMPT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-18s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("mqab.benchmark")


def get_available_languages() -> list[str]:
    """Find all languages that have test splits."""
    langs = []
    for d in sorted(TRAINING_DIR.iterdir()):
        if d.is_dir() and (d / "splits" / f"{d.name}_test.json").exists():
            langs.append(d.name)
    return langs


def run_model_benchmark(
    provider_name: str,
    model: str,
    lang: str,
    max_samples: int | None = None,
) -> dict:
    """Run a single model on one language's test split. Returns aggregated metrics."""

    test_path = TRAINING_DIR / lang / "splits" / f"{lang}_test.json"
    if not test_path.exists():
        logger.warning("No test data for %s, skipping", lang)
        return {}

    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    if max_samples:
        test_data = test_data[:max_samples]

    n = len(test_data)
    logger.info("=" * 60)
    logger.info("Benchmark: %s/%s | lang=%s | n=%d", provider_name, model, lang, n)
    logger.info("=" * 60)

    llm = get_provider(provider_name, model)
    results = []

    for i, item in enumerate(test_data):
        question = item["question"]
        context = item.get("context", "")
        gold_src = str(item.get("answer", ""))
        gold_en = str(item.get("answer_en", ""))
        context_en = item.get("context_en", "")
        question_en = item.get("question_en", "")

        # Translate if not pre-translated
        if not context_en:
            context_en = translate(context, src_lang=lang, tgt_lang="en")
        if not question_en:
            question_en = translate(question, src_lang=lang, tgt_lang="en")

        # Pipeline 1: Direct - source language context + question
        direct_prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"
        direct_response = llm.ask(direct_prompt, system_prompt=CONTEXT_SYSTEM_PROMPT)

        direct_em_src = exact_match(direct_response, gold_src)
        direct_f1_src = f1_score(direct_response, gold_src)
        direct_sim_src = semantic_similarity(direct_response, gold_src)

        # Pipeline 2: Translate-pivot - English context + question -> answer -> translate back
        translate_prompt = f"Context:\n{context_en}\n\nQuestion:\n{question_en}\n\nAnswer:\n"
        response_en = llm.ask(translate_prompt, system_prompt=CONTEXT_SYSTEM_PROMPT)
        response_src = translate(response_en, src_lang="en", tgt_lang=lang)

        pivot_em_en = exact_match(response_en, gold_en)
        pivot_f1_en = f1_score(response_en, gold_en)
        pivot_sim_en = semantic_similarity(response_en, gold_en)

        pivot_em_src = exact_match(response_src, gold_src)
        pivot_f1_src = f1_score(response_src, gold_src)
        pivot_sim_src = semantic_similarity(response_src, gold_src)

        results.append({
            "id": item.get("id", i),
            "lang": lang,
            "question": question,
            "gold_src": gold_src,
            "gold_en": gold_en,
            # Direct (source language)
            "direct_answer": direct_response,
            "direct_em_src": direct_em_src,
            "direct_f1_src": round(direct_f1_src, 4),
            "direct_sim_src": round(direct_sim_src, 4),
            # Translate-pivot (English side)
            "pivot_answer_en": response_en,
            "pivot_answer_src": response_src,
            "pivot_em_en": pivot_em_en,
            "pivot_f1_en": round(pivot_f1_en, 4),
            "pivot_sim_en": round(pivot_sim_en, 4),
            # Translate-pivot (source side)
            "pivot_em_src": pivot_em_src,
            "pivot_f1_src": round(pivot_f1_src, 4),
            "pivot_sim_src": round(pivot_sim_src, 4),
        })

        logger.info(
            "  [%d/%d] direct_sim=%.2f  pivot_sim_en=%.2f  pivot_sim_src=%.2f",
            i + 1, n, direct_sim_src, pivot_sim_en, pivot_sim_src,
        )

    # Save results
    safe_model = model.replace("/", "_")
    run_dir = RESULTS_DIR / f"benchmark_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{provider_name}_{safe_model}_{lang}"
    run_dir.mkdir(parents=True, exist_ok=True)

    results_path = run_dir / "evaluation_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    def avg(key):
        return sum(r[key] for r in results) / n

    metrics = {
        "lang": lang,
        "n_samples": n,
        "provider": provider_name,
        "model": model,
        "direct": {
            "source_side": {
                "em": round(avg("direct_em_src"), 4),
                "f1": round(avg("direct_f1_src"), 4),
                "semantic_sim": round(avg("direct_sim_src"), 4),
            },
        },
        "translate_pivot": {
            "english_side": {
                "em": round(avg("pivot_em_en"), 4),
                "f1": round(avg("pivot_f1_en"), 4),
                "semantic_sim": round(avg("pivot_sim_en"), 4),
            },
            "source_side": {
                "em": round(avg("pivot_em_src"), 4),
                "f1": round(avg("pivot_f1_src"), 4),
                "semantic_sim": round(avg("pivot_sim_src"), 4),
            },
        },
    }

    metrics_path = run_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Print summary
    d = metrics["direct"]["source_side"]
    p_en = metrics["translate_pivot"]["english_side"]
    p_src = metrics["translate_pivot"]["source_side"]
    logger.info("--- %s/%s on %s (%d samples) ---", provider_name, model, lang, n)
    logger.info("  Direct (src):        EM=%.3f  F1=%.3f  SimSem=%.3f", d["em"], d["f1"], d["semantic_sim"])
    logger.info("  Pivot (en):          EM=%.3f  F1=%.3f  SimSem=%.3f", p_en["em"], p_en["f1"], p_en["semantic_sim"])
    logger.info("  Pivot (src):         EM=%.3f  F1=%.3f  SimSem=%.3f", p_src["em"], p_src["f1"], p_src["semantic_sim"])
    logger.info("  Results -> %s", run_dir)

    return metrics


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark models on finetune test splits.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=BENCHMARK_CONFIG,
        help="Path to benchmark config (default: configs/benchmark.yaml)",
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        default=None,
        help="Run only this provider from the config",
    )
    parser.add_argument(
        "--lang", "-l",
        nargs="*",
        default=None,
        help="Language code(s) - omit for all languages with test data",
    )
    parser.add_argument(
        "--max-samples", "-n",
        type=int,
        default=None,
        help="Max test samples per language (default: all)",
    )
    args = parser.parse_args()

    # Resolve languages
    available = get_available_languages()
    if args.lang:
        langs = [l for l in args.lang if l in available]
        missing = set(args.lang) - set(available)
        if missing:
            logger.warning("No test data for: %s", ", ".join(missing))
    else:
        langs = available

    if not langs:
        logger.error("No languages with test splits found in %s", TRAINING_DIR)
        return

    # Load models from config
    config = load_config(args.config)
    models = config.get("models", [])

    # Filter by provider if specified
    if args.provider:
        models = [m for m in models if m["provider"] == args.provider]
        if not models:
            logger.error("Provider %r not found in %s", args.provider, args.config)
            return

    logger.info("Benchmarking %d model(s) on %d language(s): %s", len(models), len(langs), langs)

    all_metrics = []
    for lang in langs:
        for entry in models:
            try:
                metrics = run_model_benchmark(
                    provider_name=entry["provider"],
                    model=entry["model"],
                    lang=lang,
                    max_samples=args.max_samples,
                )
                if metrics:
                    all_metrics.append(metrics)
            except Exception:
                logger.exception("FAILED: %s/%s on %s", entry["provider"], entry["model"], lang)

    logger.info("Benchmark complete. %d runs finished.", len(all_metrics))


if __name__ == "__main__":
    main()
