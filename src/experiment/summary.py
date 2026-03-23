"""Generate SUMMARY.md from experiment results."""

import json
from pathlib import Path

from .common import logger


def _arrow(val: float) -> str:
    return "↑" if val > 0 else "↓" if val < 0 else "="


def _build_table(headers: list[str], data_rows: list[list[str]]) -> list[str]:
    """Build a column-aligned markdown table from headers and data rows."""
    col_widths = [len(h) for h in headers]
    for row in data_rows:
        for j, cell in enumerate(row):
            col_widths[j] = max(col_widths[j], len(cell))

    def fmt(cells):
        padded = [cell.ljust(col_widths[j]) for j, cell in enumerate(cells)]
        return "| " + " | ".join(padded) + " |"

    separator = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
    return [fmt(headers), separator] + [fmt(row) for row in data_rows]


def _load_run_rows(run_dir: Path) -> list[dict]:
    """Load all result JSONs in a run folder into summary rows."""
    rows = []
    for path in sorted(run_dir.glob("*.json")):
        stem = path.stem
        parts = stem.rsplit("_", 1)
        if len(parts) != 2:
            continue
        lang = parts[1]
        provider_model = parts[0]

        with open(path, "r", encoding="utf-8") as f:
            samples = json.load(f)

        n = len(samples)
        if n == 0:
            continue

        avg_direct = sum(s.get("direct_semantic_similarity", s.get("direct_sim", 0)) for s in samples) / n
        avg_translate = sum(s.get("translate_semantic_similarity", s.get("translate_sim", 0)) for s in samples) / n
        delta = avg_translate - avg_direct

        rows.append({
            "provider_model": provider_model,
            "lang": lang,
            "n": n,
            "direct_sim": avg_direct,
            "translate_sim": avg_translate,
            "delta": delta,
        })

    return rows


def _format_lang_section(lang: str, lang_rows: list[dict], headers: list[str]) -> list[str]:
    """Format a per-language results section."""
    lang_rows = sorted(lang_rows, key=lambda r: r["direct_sim"], reverse=True)
    avg_d = sum(r["direct_sim"] for r in lang_rows) / len(lang_rows)
    avg_t = sum(r["translate_sim"] for r in lang_rows) / len(lang_rows)
    avg_delta = avg_t - avg_d

    data_rows = []
    for i, r in enumerate(lang_rows, 1):
        data_rows.append([
            str(i),
            f"`{r['provider_model']}`",
            r["lang"],
            str(r["n"]),
            f"{r['direct_sim']:.4f}",
            f"{r['translate_sim']:.4f}",
            f"{r['delta']:+.4f} {_arrow(r['delta'])}",
        ])
    data_rows.append([
        "",
        "**Average**",
        "",
        "",
        f"**{avg_d:.4f}**",
        f"**{avg_t:.4f}**",
        f"**{avg_delta:+.4f}** {_arrow(avg_delta)}",
    ])

    lines = [f"## {lang.upper()}", ""]
    lines += _build_table(headers, data_rows)
    lines.append("")
    return lines


def _format_overview(rows: list[dict], langs: list[str]) -> list[str]:
    """Format the overall by-language overview table."""
    lines = ["## Overall - by Language", ""]
    overview_headers = ["Lang", "Models", "Avg Direct", "Avg Translate", "Avg Delta"]
    overview_rows = []

    for lang in langs:
        lang_rows = [r for r in rows if r["lang"] == lang]
        avg_d = sum(r["direct_sim"] for r in lang_rows) / len(lang_rows)
        avg_t = sum(r["translate_sim"] for r in lang_rows) / len(lang_rows)
        avg_delta = avg_t - avg_d
        overview_rows.append([
            lang,
            str(len(lang_rows)),
            f"{avg_d:.4f}",
            f"{avg_t:.4f}",
            f"{avg_delta:+.4f} {_arrow(avg_delta)}",
        ])

    g_d = sum(r["direct_sim"] for r in rows) / len(rows)
    g_t = sum(r["translate_sim"] for r in rows) / len(rows)
    g_delta = g_t - g_d
    overview_rows.append([
        "**ALL**",
        f"**{len(rows)}**",
        f"**{g_d:.4f}**",
        f"**{g_t:.4f}**",
        f"**{g_delta:+.4f}** {_arrow(g_delta)}",
    ])

    lines += _build_table(overview_headers, overview_rows)
    lines.append("")
    return lines


def generate_summary(run_dir: Path) -> Path:
    """Read all result JSONs in a run folder and write a SUMMARY.md table."""
    rows = _load_run_rows(run_dir)
    if not rows:
        return run_dir

    langs_seen = sorted(set(r["lang"] for r in rows))
    multi_lang = len(langs_seen) > 1
    headers = ["#", "Provider / Model", "Lang", "N", "Direct Sim", "Translate Sim", "Delta"]

    lines = [f"# Experiment Summary - {run_dir.name}", ""]

    if multi_lang:
        for lang in langs_seen:
            lang_rows = [r for r in rows if r["lang"] == lang]
            lines += _format_lang_section(lang, lang_rows, headers)
        lines += _format_overview(rows, langs_seen)
    else:
        rows.sort(key=lambda r: r["direct_sim"], reverse=True)
        lines += _format_lang_section(langs_seen[0], rows, headers)

    lines += [
        "**Direct**: LLM answers in the source language.  ",
        "**Translate**: Question -> pivot (en/fr) -> LLM -> translate back.  ",
        "**Delta**: `translate - direct` (positive = translate pipeline wins).  ",
        "**Similarity**: cosine similarity via LaBSE multilingual embeddings.",
        "",
    ]

    summary_path = run_dir / "SUMMARY.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Summary saved -> %s", summary_path)
    return summary_path
