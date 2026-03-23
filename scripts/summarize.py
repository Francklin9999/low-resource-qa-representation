"""
Generate a per-model summary table from experiment results.

Reads every JSON in data/results/**/, computes averages, and prints
a clean table. Optionally saves to CSV.

Usage:
    python scripts/summarize.py                          # latest run only
    python scripts/summarize.py --all                    # all runs
    python scripts/summarize.py --run 2026-03-19         # specific date
    python scripts/summarize.py --csv summary.csv        # also save CSV
"""

import argparse
import csv
import json
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from paths import RESULTS_DIR

logger = logging.getLogger("mqab.summarize")


def load_all(results_dir: Path) -> list[dict]:
    """Walk every date subfolder and load result JSONs."""
    entries = []
    for path in sorted(results_dir.glob("**/*.json")):
        stem = path.stem
        parts = stem.rsplit("_", 1)
        if len(parts) != 2:
            continue
        lang = parts[1]
        provider_model = parts[0]
        run_date = path.parent.name if path.parent != results_dir else "unknown"

        with open(path, "r", encoding="utf-8") as f:
            samples = json.load(f)

        if not isinstance(samples, list) or len(samples) == 0:
            continue

        n = len(samples)

        # Support both standard keys and context experiment keys
        if "direct_semantic_similarity" in samples[0]:
            avg_direct = sum(s["direct_semantic_similarity"] for s in samples) / n
            avg_translate = sum(s["translate_semantic_similarity"] for s in samples) / n
        elif "direct_sim" in samples[0] and "translate_sim" in samples[0]:
            avg_direct = sum(s["direct_sim"] for s in samples) / n
            avg_translate = sum(s["translate_sim"] for s in samples) / n
        else:
            continue

        entries.append({
            "run_date": run_date,
            "provider_model": provider_model,
            "lang": lang,
            "samples": n,
            "direct_sim": round(avg_direct, 4),
            "translate_sim": round(avg_translate, 4),
            "delta": round(avg_translate - avg_direct, 4),
        })

    return entries


def format_table(rows: list[dict]) -> str:
    """Format rows into an aligned markdown-style table."""
    if not rows:
        return "No results found."

    headers = ["Run", "Provider / Model", "Lang", "N", "Direct Sim", "Translate Sim", "Delta"]
    col_keys = ["run_date", "provider_model", "lang", "samples", "direct_sim", "translate_sim", "delta"]

    # Convert to string rows
    str_rows = []
    for r in rows:
        str_rows.append([str(r[k]) for k in col_keys])

    # Compute column widths
    widths = [len(h) for h in headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells):
        return "│ " + " │ ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " │"

    sep = "├─" + "─┼─".join("─" * w for w in widths) + "─┤"
    top = "┌─" + "─┬─".join("─" * w for w in widths) + "─┐"
    bot = "└─" + "─┴─".join("─" * w for w in widths) + "─┘"

    lines = [top, fmt_row(headers), sep]
    for row in str_rows:
        lines.append(fmt_row(row))
    lines.append(bot)

    return "\n".join(lines)


def save_csv(rows: list[dict], path: Path) -> None:
    """Save summary rows as CSV."""
    if not rows:
        return
    keys = ["run_date", "provider_model", "lang", "samples", "direct_sim", "translate_sim", "delta"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Saved CSV -> %s", path)


def main():
    parser = argparse.ArgumentParser(description="Summarize experiment results per model.")
    parser.add_argument("--all", action="store_true", help="Show all runs (default: latest only)")
    parser.add_argument("--run", type=str, default=None, help="Show a specific run date (e.g. 2026-03-19)")
    parser.add_argument("--csv", type=Path, default=None, help="Save summary to CSV file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    rows = load_all(RESULTS_DIR)
    if not rows:
        print("No results found in", RESULTS_DIR)
        return

    # Filter
    if args.run:
        rows = [r for r in rows if r["run_date"] == args.run]
    elif not args.all:
        latest = max(r["run_date"] for r in rows)
        rows = [r for r in rows if r["run_date"] == latest]

    # Sort by direct_sim descending
    rows.sort(key=lambda r: r["direct_sim"], reverse=True)

    print()
    print(format_table(rows))
    print()

    if args.csv:
        save_csv(rows, args.csv)


if __name__ == "__main__":
    main()
