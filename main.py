"""
Multilingual QA Bench - CLI entry point.

Run experiments comparing LLM performance on multilingual question answering
using direct and translate-pivot pipelines on the full AfriQA dataset.

For benchmarking on the finetune test splits, use: scripts/run_benchmark.py

Usage:
    python main.py                                       # run config (lang from config)
    python main.py --lang hau yor ibo                    # run config, 3 languages
    python main.py --lang                                # run config, ALL languages
    python main.py --config configs/benchmark.yaml       # run specific config
    python main.py --provider openai --model gpt-5.3-chat-latest --lang hau
    python main.py -p anthropic -m claude-opus-4-5-20251101 --lang hau --max-samples 50
"""

import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from data.downloader import get_languages
from paths import BENCHMARK_CONFIG
from src.experiment import run_experiment, generate_summary, create_run_dir
from utils import load_config

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-18s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("mqab")

DEFAULT_CONFIG = BENCHMARK_CONFIG
LANGUAGES = get_languages()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Multilingual QA Bench - benchmark LLMs on multilingual QA tasks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=None,
        help="Path to YAML config file (default: configs/benchmark.yaml)",
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        default=None,
        help="LLM provider name (e.g. anthropic, openai, gemini)",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Model identifier (e.g. gpt-5.3-chat-latest, claude-opus-4-5-20251101)",
    )
    parser.add_argument(
        "--lang", "-l",
        nargs="*",
        default=None,
        help="Language code(s) - e.g. --lang hau yor ibo (default: all languages)",
    )
    parser.add_argument(
        "--max-samples", "-n",
        type=int,
        default=None,
        help="Maximum number of samples to evaluate (default: all)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def resolve_langs(args, config: dict | None = None) -> list[str]:
    """Resolve language list from CLI args, falling back to config then all."""
    if args.lang:
        return args.lang
    if config:
        if config.get("languages"):
            return config["languages"]
        if config.get("language"):
            return [config["language"]]
    return sorted(LANGUAGES.keys())


def run_models(models: list[dict], langs: list[str], max_samples: int | None,
               run_dir: Path) -> None:
    """Run experiments for a list of (provider, model) pairs across languages."""
    for lang in langs:
        for entry in models:
            try:
                run_experiment(
                    provider_name=entry["provider"],
                    model=entry["model"],
                    run_dir=run_dir,
                    lang=lang,
                    max_samples=max_samples,
                )
            except Exception:
                logger.exception("SKIP %s/%s lang=%s", entry["provider"], entry["model"], lang)

    generate_summary(run_dir)


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Single-model mode
    if args.provider and args.model:
        langs = resolve_langs(args)
        logger.info("Single-model run: %s/%s | langs=%s", args.provider, args.model, langs)
        run_models(
            models=[{"provider": args.provider, "model": args.model}],
            langs=langs,
            max_samples=args.max_samples,
            run_dir=create_run_dir(),
        )
        return

    if args.provider or args.model:
        parser.error("--provider and --model must be specified together")

    # Config-file mode
    config_path = args.config or DEFAULT_CONFIG

    config = load_config(config_path)
    langs = resolve_langs(args, config)
    max_samples = args.max_samples or config.get("max_samples")
    models = config.get("models", [])

    logger.info("Loaded config: %s (%d models, langs=%s, n=%s)",
                config_path.name, len(models), langs, max_samples)
    run_models(models, langs, max_samples, create_run_dir())

    logger.info("All experiments complete.")


if __name__ == "__main__":
    main()
