"""Shared constants, data loading, and logging helpers for experiments."""

import json
import logging
from datetime import datetime
from pathlib import Path

from data.downloader import get_languages
from paths import RESULTS_DIR

logger = logging.getLogger("mqab.experiment")
LANGUAGES = get_languages()


def create_run_dir() -> Path:
    """Create a unique run directory with date + time."""
    run_dir = RESULTS_DIR / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def load_data(path: Path, max_samples: int | None = None) -> list[dict]:
    """Load a JSON data file and optionally truncate."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if max_samples:
        data = data[:max_samples]
    return data


def save_results(results: list[dict], path: Path) -> None:
    """Save experiment results to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def log_summary(results: list[dict], keys: dict[str, str], output_path: Path) -> None:
    """Log average metrics and output path.

    Args:
        results: List of result dicts.
        keys: Mapping of display_name -> result_key, e.g. {"Direct avg sim": "direct_sim"}.
        output_path: Path where results were saved.
    """
    n = len(results)
    logger.info("--- Summary ---")
    for label, key in keys.items():
        vals = [r[key] for r in results if r.get(key) is not None]
        if vals:
            logger.info("%s: %.3f", label, sum(vals) / len(vals))
    logger.info("Saved -> %s", output_path)
