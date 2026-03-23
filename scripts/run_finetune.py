"""
Fine-tuning pipeline CLI - orchestrates the full QA fine-tuning workflow.

Usage:
    # Full pipeline for one language
    python scripts/run_finetune.py all --lang fon

    # Full pipeline for ALL languages (overnight run)
    python scripts/run_finetune.py all --lang all

    # Replay: rerun only failed/incomplete languages (skips done steps)
    python scripts/run_finetune.py replay --lang all

    # Individual steps
    python scripts/run_finetune.py prepare --lang fon
    python scripts/run_finetune.py build --lang hau
    python scripts/run_finetune.py train --lang yor
    python scripts/run_finetune.py evaluate --lang fon

    # With custom config
    python scripts/run_finetune.py --config configs/finetune.yaml all --lang fon
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from paths import FINETUNE_CONFIG, DATA_DIR, TRAINING_DIR, RESULTS_DIR
from utils import load_config
from data.downloader import run as download_run, get_languages
from src.finetune.prepare import prepare_all
from src.finetune.dataset import build_training_data

from src.finetune.inference import (
    load_finetuned_model,
    run_base_model_pipeline,
    run_finetuned_pipeline,
)

from src.finetune.aya_baseline import run_aya_baseline
from src.finetune.gpu import free_gpu_memory
from src.finetune.train import TrainConfig, train
from src.evaluate import exact_match, f1_score, semantic_similarity

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-24s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("mqab.finetune")

DEFAULT_CONFIG = FINETUNE_CONFIG
LANGUAGES = get_languages()


def resolve_lang(lang_arg: str | None, config: dict) -> list[str]:
    """Resolve --lang argument to a list of language codes.

    Priority: CLI --lang > config 'language' field.
    """
    lang = lang_arg or config.get("language")
    if lang is None:
        raise ValueError(
            "No language specified. Set 'language' in the config file or pass --lang."
        )
    if lang == "all":
        return sorted(LANGUAGES.keys())
    return [lang]


def validate_config(config: dict, step: str) -> None:
    """Validate that all required config fields are present before running.

    Raises ValueError with a clear message listing all missing fields.
    """
    missing = []

    if step in ("prepare", "all"):
        data = config.get("data")
        if data is None:
            missing.append("data (section)")
        else:
            for key in ("english_source", "english_max_samples", "min_similarity", "seed"):
                if data.get(key) is None:
                    missing.append(f"data.{key}")

    if step in ("build", "all"):
        ds = config.get("dataset")
        if ds is None:
            missing.append("dataset (section)")
        else:
            for key in ("translated_ratio", "english_ratio", "augmented_ratio", "augmented_max"):
                if ds.get(key) is None:
                    missing.append(f"dataset.{key}")
        if config.get("data", {}).get("seed") is None:
            missing.append("data.seed")

    if step in ("train", "evaluate", "all"):
        train = config.get("training")
        if train is None:
            missing.append("training (section)")
        elif train.get("base_model") is None:
            missing.append("training.base_model")

    if missing:
        raise ValueError(
            f"Missing required config fields for step '{step}':\n"
            + "\n".join(f"  - {m}" for m in missing)
        )


# Step 1: Prepare


def step_prepare(config: dict, lang: str):
    """Download data with context, split, translate to English, validate."""

    data_cfg = config["data"]
    lang_name = LANGUAGES[lang]["name"]

    # Download data with context if not already present
    with_context_path = DATA_DIR / "processed" / f"{lang_name}_with_context.json"
    if not with_context_path.exists():
        logger.info("Downloading %s data with context...", lang)
        download_run(lang, with_context=True)
    else:
        logger.info("%s data with context already exists, skipping download.", lang)

    if not with_context_path.exists():
        raise FileNotFoundError(
            f"No gold passages available for {lang} in AfriQA - "
            f"cannot run the fine-tuning pipeline for this language."
        )

    stats = prepare_all(
        lang=lang,
        english_source=data_cfg["english_source"],
        english_max=data_cfg["english_max_samples"],
        min_similarity=data_cfg["min_similarity"],
        seed=data_cfg["seed"],
    )

    logger.info("Prepare complete for %s: %s", lang, json.dumps(stats, indent=2))
    return stats


# Step 2: Build Dataset


def step_build(config: dict, lang: str):
    """Build the mixed training dataset with instruction formatting."""

    ds_cfg = config["dataset"]

    stats = build_training_data(
        lang=lang,
        translated_ratio=ds_cfg["translated_ratio"],
        english_ratio=ds_cfg["english_ratio"],
        augmented_ratio=ds_cfg["augmented_ratio"],
        augmented_max=ds_cfg["augmented_max"],
        seed=config["data"]["seed"],
    )

    logger.info("Build complete for %s: %s", lang, json.dumps(stats, indent=2))
    return stats


# Step 3: Train


def step_train(_config: dict, lang: str):
    """Run QLoRA fine-tuning for a specific language."""
    tc = TrainConfig(lang=lang)

    adapter_path = train(tc)
    logger.info("Training complete for %s. Adapter saved -> %s", lang, adapter_path)
    return str(adapter_path)


# Step 4: Evaluate


def step_evaluate(config: dict, lang: str):
    """Run evaluation: fine-tuned pipeline + baselines, compute metrics."""

    eval_cfg = config.get("evaluation", {})
    base_model = config["training"]["base_model"]

    # Load test data
    test_path = TRAINING_DIR / lang / "splits" / f"{lang}_test.json"
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    max_samples = eval_cfg.get("max_samples")
    if max_samples:
        test_data = test_data[:max_samples]

    logger.info("Evaluating %s on %d test samples...", lang, len(test_data))

    # Create results directory
    run_dir = RESULTS_DIR / f"finetune_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{lang}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Load fine-tuned model for this language
    adapter_path = TRAINING_DIR / "checkpoints" / lang / "final_adapter"
    logger.info("Running fine-tuned translate-pivot pipeline...")
    model, tokenizer = load_finetuned_model(base_model=base_model, adapter_path=adapter_path)
    finetuned_preds = run_finetuned_pipeline(test_data, model, tokenizer, lang=lang)

    # Base model translate-pivot (no fine-tuning)
    logger.info("Running base model translate-pivot pipeline...")
    base_preds = run_base_model_pipeline(test_data, model, tokenizer, lang=lang)

    # Compute metrics
    results = []
    for i in range(len(test_data)):
        gold_src = str(test_data[i].get("answer", ""))
        gold_en = str(test_data[i].get("answer_en", ""))

        ft = finetuned_preds[i]
        bp = base_preds[i]

        # English-side metrics
        ft_em_en = exact_match(ft["answer_en"], gold_en)
        ft_f1_en = f1_score(ft["answer_en"], gold_en)
        ft_sim_en = semantic_similarity(ft["answer_en"], gold_en)

        bp_em_en = exact_match(bp["answer_en"], gold_en)
        bp_f1_en = f1_score(bp["answer_en"], gold_en)
        bp_sim_en = semantic_similarity(bp["answer_en"], gold_en)

        # Source-language-side metrics (end-to-end)
        ft_em_src = exact_match(ft["answer_src"], gold_src)
        ft_f1_src = f1_score(ft["answer_src"], gold_src)
        ft_sim_src = semantic_similarity(ft["answer_src"], gold_src)

        bp_em_src = exact_match(bp["answer_src"], gold_src)
        bp_f1_src = f1_score(bp["answer_src"], gold_src)
        bp_sim_src = semantic_similarity(bp["answer_src"], gold_src)

        results.append({
            "id": test_data[i].get("id", i),
            "lang": lang,
            "question": test_data[i]["question"],
            "gold_src": gold_src,
            "gold_en": gold_en,
            "ft_answer_en": ft["answer_en"],
            "ft_answer_src": ft["answer_src"],
            "ft_em_en": ft_em_en,
            "ft_f1_en": round(ft_f1_en, 4),
            "ft_sim_en": round(ft_sim_en, 4),
            "ft_em_src": ft_em_src,
            "ft_f1_src": round(ft_f1_src, 4),
            "ft_sim_src": round(ft_sim_src, 4),
            "bp_answer_en": bp["answer_en"],
            "bp_answer_src": bp["answer_src"],
            "bp_em_en": bp_em_en,
            "bp_f1_en": round(bp_f1_en, 4),
            "bp_sim_en": round(bp_sim_en, 4),
            "bp_em_src": bp_em_src,
            "bp_f1_src": round(bp_f1_src, 4),
            "bp_sim_src": round(bp_sim_src, 4),
        })

    # Save raw results
    results_path = run_dir / "evaluation_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Compute aggregates
    n = len(results)

    def avg(key):
        return sum(r[key] for r in results) / n

    metrics = {
        "lang": lang,
        "n_samples": n,
        "finetuned": {
            "english_side": {
                "em": round(avg("ft_em_en"), 4),
                "f1": round(avg("ft_f1_en"), 4),
                "semantic_sim": round(avg("ft_sim_en"), 4),
            },
            "source_side": {
                "em": round(avg("ft_em_src"), 4),
                "f1": round(avg("ft_f1_src"), 4),
                "semantic_sim": round(avg("ft_sim_src"), 4),
            },
        },
        "base_translate_pivot": {
            "english_side": {
                "em": round(avg("bp_em_en"), 4),
                "f1": round(avg("bp_f1_en"), 4),
                "semantic_sim": round(avg("bp_sim_en"), 4),
            },
            "source_side": {
                "em": round(avg("bp_em_src"), 4),
                "f1": round(avg("bp_f1_src"), 4),
                "semantic_sim": round(avg("bp_sim_src"), 4),
            },
        },
    }

    metrics_path = run_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Generate report
    _generate_report(run_dir, lang, metrics, results)

    logger.info("Evaluation complete for %s. Results -> %s", lang, run_dir)
    return metrics


def _generate_report(run_dir: Path, lang: str, metrics: dict, results: list[dict]):
    """Generate a markdown summary report."""
    n = metrics["n_samples"]
    ft = metrics["finetuned"]
    bp = metrics["base_translate_pivot"]

    lines = [
        f"# Fine-Tuning Evaluation Report - {lang.upper()}",
        f"**Run:** {run_dir.name}",
        f"**Test samples:** {n}",
        f"**Language:** {lang}",
        "",
        "## Results Summary",
        "",
        "### English-Side Metrics (isolates QA model quality)",
        "",
        "| Pipeline | EM | F1 | Semantic Sim |",
        "|----------|----|----|--------------|",
        f"| Base translate-pivot | {bp['english_side']['em']:.4f} | {bp['english_side']['f1']:.4f} | {bp['english_side']['semantic_sim']:.4f} |",
        f"| **Fine-tuned translate-pivot** | **{ft['english_side']['em']:.4f}** | **{ft['english_side']['f1']:.4f}** | **{ft['english_side']['semantic_sim']:.4f}** |",
        "",
        f"### {lang.upper()}-Side Metrics (end-to-end performance)",
        "",
        "| Pipeline | EM | F1 | Semantic Sim |",
        "|----------|----|----|--------------|",
        f"| Base translate-pivot | {bp['source_side']['em']:.4f} | {bp['source_side']['f1']:.4f} | {bp['source_side']['semantic_sim']:.4f} |",
        f"| **Fine-tuned translate-pivot** | **{ft['source_side']['em']:.4f}** | **{ft['source_side']['f1']:.4f}** | **{ft['source_side']['semantic_sim']:.4f}** |",
        "",
        "### Improvement (fine-tuned vs base)",
        "",
        f"- English EM: {ft['english_side']['em'] - bp['english_side']['em']:+.4f}",
        f"- English F1: {ft['english_side']['f1'] - bp['english_side']['f1']:+.4f}",
        f"- English Sim: {ft['english_side']['semantic_sim'] - bp['english_side']['semantic_sim']:+.4f}",
        f"- {lang.upper()} EM: {ft['source_side']['em'] - bp['source_side']['em']:+.4f}",
        f"- {lang.upper()} F1: {ft['source_side']['f1'] - bp['source_side']['f1']:+.4f}",
        f"- {lang.upper()} Sim: {ft['source_side']['semantic_sim'] - bp['source_side']['semantic_sim']:+.4f}",
        "",
        "## Sample Predictions",
        "",
    ]

    for r in results[:10]:
        lines.extend([
            f"### {r['id']}",
            f"- **Question:** {r['question']}",
            f"- **Gold ({lang}):** {r['gold_src']}",
            f"- **Gold (EN):** {r['gold_en']}",
            f"- **Fine-tuned (EN):** {r['ft_answer_en']} (sim={r['ft_sim_en']:.3f})",
            f"- **Fine-tuned ({lang}):** {r['ft_answer_src']} (sim={r['ft_sim_src']:.3f})",
            f"- **Base (EN):** {r['bp_answer_en']} (sim={r['bp_sim_en']:.3f})",
            f"- **Base ({lang}):** {r['bp_answer_src']} (sim={r['bp_sim_src']:.3f})",
            "",
        ])

    report_path = run_dir / "REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Report saved -> %s", report_path)


# Step 5: Aya Baseline


def step_aya(config: dict, lang: str):
    """Run Aya-23-8B baseline: direct + translate-pivot, compute metrics."""

    eval_cfg = config.get("evaluation", {})

    # Load test data
    test_path = TRAINING_DIR / lang / "splits" / f"{lang}_test.json"
    if not test_path.exists():
        logger.warning("No test split for %s - skipping. Run 'prepare' first.", lang)
        return None
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    max_samples = eval_cfg.get("max_samples")
    if max_samples:
        test_data = test_data[:max_samples]

    logger.info("Running Aya-23-8B baseline for %s on %d test samples...", lang, len(test_data))

    # Create results directory
    run_dir = RESULTS_DIR / f"aya_baseline_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{lang}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Run Aya baselines (both direct and translate-pivot)
    aya_results = run_aya_baseline(test_data, lang=lang)

    # Free GPU before loading LaBSE for semantic similarity
    free_gpu_memory()

    # Compute metrics
    results = []
    for i in range(len(test_data)):
        gold_src = str(test_data[i].get("answer", ""))
        gold_en = str(test_data[i].get("answer_en", ""))

        direct = aya_results["direct"][i]
        pivot = aya_results["translate_pivot"][i]

        # Direct: Aya answers in source language
        direct_em_src = exact_match(direct["answer_src"], gold_src)
        direct_f1_src = f1_score(direct["answer_src"], gold_src)
        direct_sim_src = semantic_similarity(direct["answer_src"], gold_src)

        # Translate-pivot: English-side
        pivot_em_en = exact_match(pivot["answer_en"], gold_en)
        pivot_f1_en = f1_score(pivot["answer_en"], gold_en)
        pivot_sim_en = semantic_similarity(pivot["answer_en"], gold_en)

        # Translate-pivot: Source-side (end-to-end)
        pivot_em_src = exact_match(pivot["answer_src"], gold_src)
        pivot_f1_src = f1_score(pivot["answer_src"], gold_src)
        pivot_sim_src = semantic_similarity(pivot["answer_src"], gold_src)

        results.append({
            "id": test_data[i].get("id", i),
            "lang": lang,
            "question": test_data[i]["question"],
            "gold_src": gold_src,
            "gold_en": gold_en,
            "aya_direct_answer": direct["answer_src"],
            "aya_direct_em": direct_em_src,
            "aya_direct_f1": round(direct_f1_src, 4),
            "aya_direct_sim": round(direct_sim_src, 4),
            "aya_pivot_answer_en": pivot["answer_en"],
            "aya_pivot_answer_src": pivot["answer_src"],
            "aya_pivot_em_en": pivot_em_en,
            "aya_pivot_f1_en": round(pivot_f1_en, 4),
            "aya_pivot_sim_en": round(pivot_sim_en, 4),
            "aya_pivot_em_src": pivot_em_src,
            "aya_pivot_f1_src": round(pivot_f1_src, 4),
            "aya_pivot_sim_src": round(pivot_sim_src, 4),
        })

    # Save raw results
    results_path = run_dir / "evaluation_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Compute aggregates
    n = len(results)

    def avg(key):
        return sum(r[key] for r in results) / n

    metrics = {
        "lang": lang,
        "n_samples": n,
        "model": "Aya-23-8B",
        "aya_direct": {
            "source_side": {
                "em": round(avg("aya_direct_em"), 4),
                "f1": round(avg("aya_direct_f1"), 4),
                "semantic_sim": round(avg("aya_direct_sim"), 4),
            },
        },
        "aya_translate_pivot": {
            "english_side": {
                "em": round(avg("aya_pivot_em_en"), 4),
                "f1": round(avg("aya_pivot_f1_en"), 4),
                "semantic_sim": round(avg("aya_pivot_sim_en"), 4),
            },
            "source_side": {
                "em": round(avg("aya_pivot_em_src"), 4),
                "f1": round(avg("aya_pivot_f1_src"), 4),
                "semantic_sim": round(avg("aya_pivot_sim_src"), 4),
            },
        },
    }

    metrics_path = run_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Generate report
    _generate_aya_report(run_dir, lang, metrics, results)

    logger.info("Aya baseline complete for %s. Results -> %s", lang, run_dir)
    return metrics


def _generate_aya_report(run_dir: Path, lang: str, metrics: dict, results: list[dict]):
    """Generate a markdown report for Aya baseline."""
    n = metrics["n_samples"]
    direct = metrics["aya_direct"]
    pivot = metrics["aya_translate_pivot"]

    lines = [
        f"# Aya-23-8B Baseline Report - {lang.upper()}",
        f"**Run:** {run_dir.name}",
        f"**Test samples:** {n}",
        f"**Language:** {lang}",
        f"**Model:** Aya-23-8B (4-bit quantized)",
        "",
        "## Results Summary",
        "",
        f"### {lang.upper()}-Side Metrics",
        "",
        "| Pipeline | EM | F1 | Semantic Sim |",
        "|----------|----|----|--------------|",
        f"| Aya direct ({lang}) | {direct['source_side']['em']:.4f} | {direct['source_side']['f1']:.4f} | {direct['source_side']['semantic_sim']:.4f} |",
        f"| Aya translate-pivot | {pivot['source_side']['em']:.4f} | {pivot['source_side']['f1']:.4f} | {pivot['source_side']['semantic_sim']:.4f} |",
        "",
        "### English-Side Metrics (translate-pivot only)",
        "",
        "| Pipeline | EM | F1 | Semantic Sim |",
        "|----------|----|----|--------------|",
        f"| Aya translate-pivot | {pivot['english_side']['em']:.4f} | {pivot['english_side']['f1']:.4f} | {pivot['english_side']['semantic_sim']:.4f} |",
        "",
        "## Sample Predictions",
        "",
    ]

    for r in results[:10]:
        lines.extend([
            f"### {r['id']}",
            f"- **Question:** {r['question']}",
            f"- **Gold ({lang}):** {r['gold_src']}",
            f"- **Aya direct:** {r['aya_direct_answer']} (sim={r['aya_direct_sim']:.3f})",
            f"- **Aya pivot (EN):** {r['aya_pivot_answer_en']} (sim={r['aya_pivot_sim_en']:.3f})",
            f"- **Aya pivot ({lang}):** {r['aya_pivot_answer_src']} (sim={r['aya_pivot_sim_src']:.3f})",
            "",
        ])

    report_path = run_dir / "REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Aya report saved -> %s", report_path)


# Step completion detection


def is_step_done(step: str, lang: str) -> bool:
    """Check if a pipeline step has already completed for a language."""
    if step == "prepare":
        splits_dir = TRAINING_DIR / lang / "splits"
        return all(
            (splits_dir / f"{lang}_{split}.json").exists()
            for split in ("train", "val", "test")
        )
    if step == "build":
        lang_dir = TRAINING_DIR / lang
        return (lang_dir / "train.jsonl").exists() and (lang_dir / "val.jsonl").exists()
    if step == "train":
        adapter_dir = TRAINING_DIR / "checkpoints" / lang / "final_adapter"
        return adapter_dir.exists() and (adapter_dir / "adapter_config.json").exists()
    if step == "evaluate":
        # Look for any finetune results directory for this lang that has metrics.json
        if RESULTS_DIR.exists():
            for d in RESULTS_DIR.iterdir():
                if d.is_dir() and d.name.startswith("finetune_") and d.name.endswith(f"_{lang}"):
                    if (d / "metrics.json").exists():
                        return True
        return False
    if step == "aya":
        if RESULTS_DIR.exists():
            for d in RESULTS_DIR.iterdir():
                if d.is_dir() and d.name.startswith("aya_baseline_") and d.name.endswith(f"_{lang}"):
                    if (d / "metrics.json").exists():
                        return True
        return False
    return False


# CLI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fine-tuning pipeline for multilingual QA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "step",
        choices=["prepare", "build", "train", "evaluate", "aya", "all", "replay"],
        help="Pipeline step to run ('replay' to rerun only failed languages)",
    )
    parser.add_argument(
        "--lang", "-l",
        type=str,
        default=None,
        help="Language code (e.g. fon, hau, yor) or 'all' for all languages. "
             "Falls back to 'language' in config if not provided.",
    )
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=DEFAULT_CONFIG,
        help=f"Config file (default: {DEFAULT_CONFIG})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def run_pipeline_for_lang(lang: str, step: str, config: dict, skip_done: bool = False):
    """Run one or all pipeline steps for a single language."""
    steps_order = ["prepare", "build", "train", "evaluate"]

    steps = {
        "prepare": step_prepare,
        "build": step_build,
        "train": step_train,
        "evaluate": step_evaluate,
        "aya": step_aya,
    }

    if step == "all":
        run_steps = steps_order
    else:
        run_steps = [step]

    for name in run_steps:
        if skip_done and is_step_done(name, lang):
            logger.info("SKIP: %s for %s (already done)", name.upper(), lang.upper())
            continue

        logger.info("=" * 60)
        logger.info("STEP: %s | LANG: %s", name.upper(), lang.upper())
        logger.info("=" * 60)
        try:
            steps[name](config, lang)
        except Exception:
            logger.exception("FAILED: %s for %s", name, lang)
            if step not in ("all", "replay"):
                raise
            logger.info("Skipping remaining steps for %s", lang)
            break


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    config = load_config(args.config)

    # replay is treated as "all" but with skip_done=True
    effective_step = "all" if args.step == "replay" else args.step
    skip_done = args.step == "replay"

    langs = resolve_lang(args.lang, config)
    validate_config(config, effective_step)

    if skip_done:
        # Show status before starting
        for lang in langs:
            done = [s for s in ("prepare", "build", "train", "evaluate") if is_step_done(s, lang)]
            todo = [s for s in ("prepare", "build", "train", "evaluate") if not is_step_done(s, lang)]
            logger.info("  %s: done=%s | todo=%s", lang.upper(), done or "none", todo or "all done")

    logger.info("Config: %s | Step: %s | Languages: %s", args.config, effective_step, langs)

    for lang in langs:
        if skip_done and all(is_step_done(s, lang) for s in ("prepare", "build", "train", "evaluate")):
            logger.info("SKIP %s - all steps already complete", lang.upper())
            continue

        logger.info("*" * 60)
        logger.info("LANGUAGE: %s", lang.upper())
        logger.info("*" * 60)
        run_pipeline_for_lang(lang, effective_step, config, skip_done=skip_done)

    logger.info("All done.")


if __name__ == "__main__":
    main()
