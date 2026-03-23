"""
Unified analysis: compare Finetuned QLoRA, Base Qwen, Aya-23-8B, and all
benchmark models across all languages.

Display names for models are loaded from configs/benchmark.yaml.

Usage:
    python scripts/analyze.py                    # tables only
    python scripts/analyze.py --plot             # tables + plots
    python scripts/analyze.py --finetune         # finetune-only tables/plots
    python scripts/analyze.py --benchmark        # benchmark-only tables/plots
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import yaml
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from paths import RESULTS_DIR, LANGUAGES_CONFIG, BENCHMARK_CONFIG, ROOT

logger = logging.getLogger("mqab.analyze")

# Config-driven helpers

def _load_lang_names() -> dict[str, str]:
    if not LANGUAGES_CONFIG.exists():
        return {}
    with open(LANGUAGES_CONFIG, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return {
        code: info["name"].capitalize()
        for code, info in cfg.get("languages", {}).items()
    }


def _load_model_display_names() -> dict[str, str]:
    """Load model_id -> display_name mapping from benchmark.yaml."""
    if not BENCHMARK_CONFIG.exists():
        return {}
    with open(BENCHMARK_CONFIG, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    mapping = {}
    for entry in cfg.get("models", []):
        model_id = entry.get("model", "")
        display = entry.get("display_name", model_id)
        mapping[model_id] = display
    return mapping


def _load_other_model_names() -> dict[str, str]:
    """Load display names for non-benchmark models (finetuned, base, aya)."""
    if not BENCHMARK_CONFIG.exists():
        return {"finetuned": "Finetuned QLoRA", "base_qwen": "Base Qwen2.5-3B", "aya": "Aya-23-8B"}
    with open(BENCHMARK_CONFIG, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    defaults = {"finetuned": "Finetuned QLoRA", "base_qwen": "Base Qwen2.5-3B", "aya": "Aya-23-8B"}
    return cfg.get("other_models", defaults)


def _short(model_id: str, display_map: dict[str, str]) -> str:
    return display_map.get(model_id, model_id)


# Loaders

def load_finetune_results(results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    lang_names = _load_lang_names()
    records = []
    for mp in sorted(results_dir.glob("finetune_*/metrics.json")):
        folder = mp.parent.name
        m = re.match(r"finetune_(\d{4}-\d{2}-\d{2})_[\d-]+_(\w+)", folder)
        if not m:
            continue
        with open(mp, "r", encoding="utf-8") as f:
            data = json.load(f)
        lang = m.group(2)
        ft = data.get("finetuned", {})
        bp = data.get("base_translate_pivot", {})
        records.append({
            "lang": lang,
            "lang_name": lang_names.get(lang, lang),
            "n_samples": data.get("n_samples", 0),
            "ft_em_en": ft.get("english_side", {}).get("em", 0),
            "ft_f1_en": ft.get("english_side", {}).get("f1", 0),
            "ft_sim_en": ft.get("english_side", {}).get("semantic_sim", 0),
            "ft_em_src": ft.get("source_side", {}).get("em", 0),
            "ft_f1_src": ft.get("source_side", {}).get("f1", 0),
            "ft_sim_src": ft.get("source_side", {}).get("semantic_sim", 0),
            "bp_em_en": bp.get("english_side", {}).get("em", 0),
            "bp_f1_en": bp.get("english_side", {}).get("f1", 0),
            "bp_sim_en": bp.get("english_side", {}).get("semantic_sim", 0),
            "bp_em_src": bp.get("source_side", {}).get("em", 0),
            "bp_f1_src": bp.get("source_side", {}).get("f1", 0),
            "bp_sim_src": bp.get("source_side", {}).get("semantic_sim", 0),
        })
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset="lang", keep="last")
    return df


def load_aya_results(results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    lang_names = _load_lang_names()
    records = []
    for mp in sorted(results_dir.glob("aya_baseline_*/metrics.json")):
        folder = mp.parent.name
        m = re.match(r"aya_baseline_(\d{4}-\d{2}-\d{2})_[\d-]+_(\w+)", folder)
        if not m:
            continue
        with open(mp, "r", encoding="utf-8") as f:
            data = json.load(f)
        lang = m.group(2)
        direct = data.get("aya_direct", {})
        pivot = data.get("aya_translate_pivot", {})
        records.append({
            "lang": lang,
            "lang_name": lang_names.get(lang, lang),
            "aya_dir_em_src": direct.get("source_side", {}).get("em", 0),
            "aya_dir_f1_src": direct.get("source_side", {}).get("f1", 0),
            "aya_dir_sim_src": direct.get("source_side", {}).get("semantic_sim", 0),
            "aya_piv_em_en": pivot.get("english_side", {}).get("em", 0),
            "aya_piv_f1_en": pivot.get("english_side", {}).get("f1", 0),
            "aya_piv_sim_en": pivot.get("english_side", {}).get("semantic_sim", 0),
            "aya_piv_em_src": pivot.get("source_side", {}).get("em", 0),
            "aya_piv_f1_src": pivot.get("source_side", {}).get("f1", 0),
            "aya_piv_sim_src": pivot.get("source_side", {}).get("semantic_sim", 0),
        })
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset="lang", keep="last")
    return df


def load_benchmark_results(results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    """Load benchmark_*/metrics.json into a DataFrame (one row per model+lang)."""
    lang_names = _load_lang_names()
    display_map = _load_model_display_names()
    records = []
    for mp in sorted(results_dir.glob("benchmark_*/metrics.json")):
        with open(mp, "r", encoding="utf-8") as f:
            data = json.load(f)
        lang = data.get("lang", "")
        model = data.get("model", "")
        provider = data.get("provider", "")
        direct = data.get("direct", {})
        pivot = data.get("translate_pivot", {})
        records.append({
            "lang": lang,
            "lang_name": lang_names.get(lang, lang),
            "provider": provider,
            "model": model,
            "model_short": _short(model, display_map),
            "dir_em_src": direct.get("source_side", {}).get("em", 0),
            "dir_f1_src": direct.get("source_side", {}).get("f1", 0),
            "dir_sim_src": direct.get("source_side", {}).get("semantic_sim", 0),
            "piv_em_en": pivot.get("english_side", {}).get("em", 0),
            "piv_f1_en": pivot.get("english_side", {}).get("f1", 0),
            "piv_sim_en": pivot.get("english_side", {}).get("semantic_sim", 0),
            "piv_em_src": pivot.get("source_side", {}).get("em", 0),
            "piv_f1_src": pivot.get("source_side", {}).get("f1", 0),
            "piv_sim_src": pivot.get("source_side", {}).get("semantic_sim", 0),
        })
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset=["lang", "model"], keep="last")
    return df


def build_unified_df(ft_df, aya_df, bench_df):
    """Build a unified long-form DataFrame: one row per (model, lang, side)."""
    lang_names = _load_lang_names()
    other_names = _load_other_model_names()
    rows = []

    def _add(model_name, lang, side, em, f1, sim, pipeline):
        rows.append({
            "model": model_name, "lang": lang,
            "lang_name": lang_names.get(lang, lang),
            "side": side, "pipeline": pipeline,
            "em": em, "f1": f1, "sim": sim,
        })

    ft_name = other_names.get("finetuned", "Finetuned QLoRA")
    base_name = other_names.get("base_qwen", "Base Qwen2.5-3B")
    aya_name = other_names.get("aya", "Aya-23-8B")

    for _, r in ft_df.iterrows():
        lang = r["lang"]
        _add(ft_name, lang, "english", r["ft_em_en"], r["ft_f1_en"], r["ft_sim_en"], "translate-pivot")
        _add(ft_name, lang, "source", r["ft_em_src"], r["ft_f1_src"], r["ft_sim_src"], "direct")
        _add(base_name, lang, "english", r["bp_em_en"], r["bp_f1_en"], r["bp_sim_en"], "translate-pivot")
        _add(base_name, lang, "source", r["bp_em_src"], r["bp_f1_src"], r["bp_sim_src"], "translate-pivot")

    if not aya_df.empty:
        for _, r in aya_df.iterrows():
            lang = r["lang"]
            _add(aya_name, lang, "source", r["aya_dir_em_src"], r["aya_dir_f1_src"], r["aya_dir_sim_src"], "direct")
            _add(aya_name, lang, "english", r["aya_piv_em_en"], r["aya_piv_f1_en"], r["aya_piv_sim_en"], "translate-pivot")

    if not bench_df.empty:
        for _, r in bench_df.iterrows():
            lang = r["lang"]
            name = r["model_short"]
            _add(name, lang, "source", r["dir_em_src"], r["dir_f1_src"], r["dir_sim_src"], "direct")
            _add(name, lang, "english", r["piv_em_en"], r["piv_f1_en"], r["piv_sim_en"], "translate-pivot")

    return pd.DataFrame(rows)


# Pretty-print

def _sep(w=120):
    return "\u2500" * w

def _header(title, w=120):
    pad = max(0, (w - len(title) - 2) // 2)
    return f"\n{'=' * w}\n{' ' * pad} {title}\n{'=' * w}"

def _pct(v):
    return f"{v * 100:5.1f}%"


def print_unified_table(udf: pd.DataFrame, side: str, title: str) -> None:
    sub = udf[udf["side"] == side]
    if sub.empty:
        return

    other_names = _load_other_model_names()
    ft_name = other_names.get("finetuned", "Finetuned QLoRA")
    base_name = other_names.get("base_qwen", "Base Qwen2.5-3B")
    aya_name = other_names.get("aya", "Aya-23-8B")

    models = sub["model"].unique().tolist()
    priority = [ft_name, base_name, aya_name]
    ordered = [m for m in priority if m in models] + [m for m in models if m not in priority]

    langs = sorted(sub["lang"].unique())
    lang_names = _load_lang_names()

    col_w = 28
    W = 20 + len(ordered) * (col_w + 3)

    print(_header(title))
    print()

    hdr = f"  {'Language':<16} "
    sub_hdr = f"  {'':16} "
    for model in ordered:
        hdr += f"| {model:^{col_w}} "
        sub_hdr += f"| {'EM':>7} {'F1':>7} {'SimSem':>8}   "
    print(hdr + "|")
    print(sub_hdr + "|")
    print(f"  {_sep(W)}")

    for lang in langs:
        lname = lang_names.get(lang, lang)
        line = f"  {lname:<16} "
        for model in ordered:
            row = sub[(sub["lang"] == lang) & (sub["model"] == model)]
            if row.empty:
                line += f"| {'---':>7} {'---':>7} {'---':>8}   "
            else:
                r = row.iloc[0]
                line += f"| {_pct(r['em'])} {_pct(r['f1'])} {_pct(r['sim'])}   "
        print(line + "|")

    print(f"  {_sep(W)}")

    line = f"  {'MACRO AVG':<16} "
    for model in ordered:
        msub = sub[sub["model"] == model]
        if msub.empty:
            line += f"| {'---':>7} {'---':>7} {'---':>8}   "
        else:
            line += f"| {_pct(msub['em'].mean())} {_pct(msub['f1'].mean())} {_pct(msub['sim'].mean())}   "
    print(line + "|")
    print()


def print_delta_table(udf: pd.DataFrame, ref_model: str, side: str, title: str) -> None:
    sub = udf[udf["side"] == side]
    if sub.empty:
        return

    models = [m for m in sub["model"].unique() if m != ref_model]
    langs = sorted(sub["lang"].unique())
    lang_names = _load_lang_names()

    col_w = 28
    W = 20 + len(models) * (col_w + 3)

    print(_header(title))
    print()

    hdr = f"  {'Language':<16} "
    sub_hdr = f"  {'':16} "
    for model in models:
        hdr += f"| {model:^{col_w}} "
        sub_hdr += f"| {'dEM':>7} {'dF1':>7} {'dSimSem':>9}  "
    print(hdr + "|")
    print(sub_hdr + "|")
    print(f"  {_sep(W)}")

    for lang in langs:
        lname = lang_names.get(lang, lang)
        ref = sub[(sub["lang"] == lang) & (sub["model"] == ref_model)]
        line = f"  {lname:<16} "
        for model in models:
            row = sub[(sub["lang"] == lang) & (sub["model"] == model)]
            if row.empty or ref.empty:
                line += f"| {'---':>7} {'---':>7} {'---':>9}  "
            else:
                rr = ref.iloc[0]
                mr = row.iloc[0]
                line += (
                    f"| {(mr['em'] - rr['em'])*100:>+6.1f} "
                    f"{(mr['f1'] - rr['f1'])*100:>+6.1f} "
                    f"{(mr['sim'] - rr['sim'])*100:>+8.1f}  "
                )
        print(line + "|")

    print(f"  {_sep(W)}")

    line = f"  {'MACRO AVG':<16} "
    for model in models:
        msub = sub[sub["model"] == model]
        rsub = sub[sub["model"] == ref_model]
        if msub.empty or rsub.empty:
            line += f"| {'---':>7} {'---':>7} {'---':>9}  "
        else:
            merged = msub.set_index("lang")[["em", "f1", "sim"]].subtract(
                rsub.set_index("lang")[["em", "f1", "sim"]]
            ).mean()
            line += (
                f"| {merged['em']*100:>+6.1f} "
                f"{merged['f1']*100:>+6.1f} "
                f"{merged['sim']*100:>+8.1f}  "
            )
    print(line + "|")
    print()


# Plots

def _model_palette(models):
    base_colors = [
        "#2196F3", "#FF7043", "#66BB6A", "#AB47BC", "#EC407A",
        "#26C6DA", "#FFA726", "#78909C", "#D4E157", "#8D6E63",
    ]
    return {m: base_colors[i % len(base_colors)] for i, m in enumerate(models)}


def _get_models_ordered(udf):
    """Return model list with finetune/base/aya first, then benchmark models."""
    other_names = _load_other_model_names()
    priority = [
        other_names.get("finetuned", "Finetuned QLoRA"),
        other_names.get("base_qwen", "Base Qwen2.5-3B"),
        other_names.get("aya", "Aya-23-8B"),
    ]
    all_models = udf["model"].unique().tolist()
    ordered = [m for m in priority if m in all_models]
    ordered += [m for m in all_models if m not in ordered]
    return ordered


def generate_unified_plots(udf: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=1.1)

    models_ordered = _get_models_ordered(udf)
    palette = _model_palette(models_ordered)
    other_names = _load_other_model_names()
    ft_name = other_names.get("finetuned", "Finetuned QLoRA")

    src = udf[udf["side"] == "source"].copy()
    en = udf[udf["side"] == "english"].copy()

    # Plot 1: Source-side SimSem bar chart
    if not src.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(
            data=src, x="lang_name", y="sim", hue="model",
            hue_order=models_ordered, palette=palette, ax=ax,
        )
        ax.set_title(
            "Source-Language Semantic Similarity - All Models\n"
            "Direct answers evaluated against gold answers in the source language",
            fontsize=13, fontweight="bold",
        )
        ax.set_xlabel("Target Language", fontsize=11)
        ax.set_ylabel("Semantic Similarity (LaBSE cosine, 0-1)", fontsize=11)
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=30)
        ax.legend(title="Model", loc="upper right", fontsize=7, title_fontsize=9)
        fig.text(
            0.5, -0.03,
            "Semantic Similarity: cosine similarity between LaBSE embeddings of predicted and gold answers.\n"
            "Higher = predicted answer is semantically closer to the gold answer.",
            ha="center", fontsize=8, style="italic", color="grey",
        )
        fig.tight_layout()
        path = output_dir / "all_models_source_sim.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 2: English-side SimSem bar chart
    if not en.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(
            data=en, x="lang_name", y="sim", hue="model",
            hue_order=models_ordered, palette=palette, ax=ax,
        )
        ax.set_title(
            "English-Side Semantic Similarity - All Models (Translate-Pivot)\n"
            "Answers translated to English, evaluated against English gold answers",
            fontsize=13, fontweight="bold",
        )
        ax.set_xlabel("Target Language", fontsize=11)
        ax.set_ylabel("Semantic Similarity (LaBSE cosine, 0-1)", fontsize=11)
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=30)
        ax.legend(title="Model", loc="upper right", fontsize=7, title_fontsize=9)
        fig.tight_layout()
        path = output_dir / "all_models_english_sim.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 3: All 3 metrics, source side, grouped
    if not src.empty:
        melted = src.melt(
            id_vars=["model", "lang_name"],
            value_vars=["em", "f1", "sim"],
            var_name="metric", value_name="score",
        )
        melted["metric"] = melted["metric"].map({
            "em": "Exact Match", "f1": "F1 Score", "sim": "Semantic Similarity",
        })
        fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharey=True)
        fig.suptitle(
            "Source-Language Evaluation - All Models & Metrics",
            fontsize=14, fontweight="bold", y=1.02,
        )
        for ax, metric_name in zip(axes, ["Exact Match", "F1 Score", "Semantic Similarity"]):
            mdata = melted[melted["metric"] == metric_name]
            sns.barplot(
                data=mdata, x="lang_name", y="score", hue="model",
                hue_order=models_ordered, palette=palette, ax=ax,
            )
            ax.set_title(metric_name, fontsize=12, fontweight="bold")
            ax.set_xlabel("Language", fontsize=10)
            ax.set_ylabel("Score (0-1)", fontsize=10)
            ax.set_ylim(0, 1)
            ax.tick_params(axis="x", rotation=45)
            if ax != axes[0]:
                ax.get_legend().remove()
            else:
                ax.legend(title="Model", fontsize=6, title_fontsize=8, loc="upper left")
        fig.tight_layout()
        path = output_dir / "all_models_source_metrics.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 4: Heatmap - SimSem source, model x language
    if not src.empty:
        pivot = src.pivot_table(
            index="lang_name", columns="model", values="sim", aggfunc="mean",
        )
        cols = [m for m in models_ordered if m in pivot.columns]
        pivot = pivot[cols]

        fig, ax = plt.subplots(figsize=(max(10, len(cols) * 1.8), 7))
        sns.heatmap(
            pivot, annot=True, fmt=".2f", cmap="YlGnBu",
            linewidths=0.5, ax=ax, vmin=0, vmax=1,
            cbar_kws={"label": "Semantic Similarity (0-1)"},
            annot_kws={"fontsize": 10},
        )
        ax.set_title(
            "Source-Language Semantic Similarity - Model x Language Heatmap\n"
            "Darker = higher semantic similarity with gold answer",
            fontsize=13, fontweight="bold",
        )
        ax.set_ylabel("Language", fontsize=11)
        ax.set_xlabel("Model", fontsize=11)
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        path = output_dir / "heatmap_source_sim.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 5: Heatmap - SimSem english side
    if not en.empty:
        pivot_en = en.pivot_table(
            index="lang_name", columns="model", values="sim", aggfunc="mean",
        )
        cols = [m for m in models_ordered if m in pivot_en.columns]
        pivot_en = pivot_en[cols]

        fig, ax = plt.subplots(figsize=(max(10, len(cols) * 1.8), 7))
        sns.heatmap(
            pivot_en, annot=True, fmt=".2f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, vmin=0, vmax=1,
            cbar_kws={"label": "Semantic Similarity (0-1)"},
            annot_kws={"fontsize": 10},
        )
        ax.set_title(
            "English-Side Semantic Similarity - Model x Language Heatmap\n"
            "(translate-pivot pipeline, evaluated against English gold answer)",
            fontsize=13, fontweight="bold",
        )
        ax.set_ylabel("Language", fontsize=11)
        ax.set_xlabel("Model", fontsize=11)
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        path = output_dir / "heatmap_english_sim.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 6: Delta heatmap - each model vs Finetuned (source SimSem)
    if not src.empty and ft_name in src["model"].values:
        ft_pivot = src[src["model"] == ft_name].set_index("lang_name")["sim"]
        others = [m for m in models_ordered if m != ft_name]
        delta_data = {}
        for model in others:
            msub = src[src["model"] == model].set_index("lang_name")["sim"]
            delta_data[model] = (msub - ft_pivot) * 100

        delta_df = pd.DataFrame(delta_data).dropna(how="all")

        if not delta_df.empty:
            fig, ax = plt.subplots(figsize=(max(10, len(others) * 1.8), 7))
            sns.heatmap(
                delta_df, annot=True, fmt="+.1f", center=0,
                cmap="RdYlGn_r", linewidths=0.5, ax=ax,
                cbar_kws={"label": "Difference (pp)"},
                annot_kws={"fontsize": 10},
            )
            ax.set_title(
                f"Source SimSem: Each Model minus {ft_name} (percentage points)\n"
                f"Green = model beats finetuned.  Red = finetuned wins.",
                fontsize=13, fontweight="bold",
            )
            ax.set_ylabel("Language", fontsize=11)
            ax.set_xlabel("Model", fontsize=11)
            ax.tick_params(axis="x", rotation=30)
            fig.tight_layout()
            path = output_dir / "delta_vs_finetuned_source.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            plt.close(fig)
            logger.info("Saved -> %s", path)

    # Plot 7: Radar chart - macro-average per model
    if not udf.empty:
        categories = ["EM\n(Source)", "F1\n(Source)", "SimSem\n(Source)",
                       "EM\n(English)", "F1\n(English)", "SimSem\n(English)"]
        n_cats = len(categories)
        angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"polar": True})

        for model in models_ordered:
            src_m = udf[(udf["model"] == model) & (udf["side"] == "source")]
            en_m = udf[(udf["model"] == model) & (udf["side"] == "english")]
            if src_m.empty and en_m.empty:
                continue
            vals = [
                src_m["em"].mean() if not src_m.empty else 0,
                src_m["f1"].mean() if not src_m.empty else 0,
                src_m["sim"].mean() if not src_m.empty else 0,
                en_m["em"].mean() if not en_m.empty else 0,
                en_m["f1"].mean() if not en_m.empty else 0,
                en_m["sim"].mean() if not en_m.empty else 0,
            ]
            vals += vals[:1]
            color = palette.get(model, "#888888")
            ax.fill(angles, vals, alpha=0.1, color=color)
            ax.plot(angles, vals, "o-", color=color, linewidth=2, label=model, markersize=5)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], size=8, color="grey")
        ax.set_title(
            "Macro-Average Performance Radar - All Models\n"
            "(averaged across all languages)",
            fontsize=13, fontweight="bold", pad=30,
        )
        ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8, title="Model")
        fig.tight_layout()
        path = output_dir / "radar_all_models.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 8: Box plot - distribution across languages
    if not src.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(
            data=src, x="model", y="sim", order=models_ordered,
            palette=palette, ax=ax,
        )
        sns.stripplot(
            data=src, x="model", y="sim", order=models_ordered,
            color="black", size=4, alpha=0.5, ax=ax,
        )
        ax.set_title(
            "Distribution of Source-Language Semantic Similarity across Languages\n"
            "Box = IQR, whiskers = 1.5x IQR, dots = individual languages",
            fontsize=13, fontweight="bold",
        )
        ax.set_xlabel("Model", fontsize=11)
        ax.set_ylabel("Semantic Similarity (0-1)", fontsize=11)
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        path = output_dir / "boxplot_source_sim.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)

    # Plot 9: Macro-average summary bar chart
    if not udf.empty:
        macro = udf.groupby(["model", "side"]).agg(
            em=("em", "mean"), f1=("f1", "mean"), sim=("sim", "mean"),
        ).reset_index()

        src_macro = macro[macro["side"] == "source"].copy()
        valid = [m for m in models_ordered if m in src_macro["model"].values]
        src_macro = src_macro.set_index("model").loc[valid].reset_index()

        if not src_macro.empty:
            melted = src_macro.melt(
                id_vars=["model"], value_vars=["em", "f1", "sim"],
                var_name="metric", value_name="score",
            )
            melted["metric"] = melted["metric"].map({
                "em": "Exact Match", "f1": "F1 Score", "sim": "Semantic Sim",
            })
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(
                data=melted, x="model", y="score", hue="metric",
                palette=["#42A5F5", "#66BB6A", "#FFA726"], ax=ax,
            )
            ax.set_title(
                "Macro-Average Source-Language Scores - All Models\n"
                "Averaged across all low-resource African languages",
                fontsize=13, fontweight="bold",
            )
            ax.set_xlabel("Model", fontsize=11)
            ax.set_ylabel("Score (0-1)", fontsize=11)
            ax.set_ylim(0, 1)
            ax.tick_params(axis="x", rotation=30)
            ax.legend(title="Metric", fontsize=9)
            for container in ax.containers:
                ax.bar_label(container, fmt="%.2f", fontsize=7, padding=2)
            fig.tight_layout()
            path = output_dir / "macro_avg_source.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            plt.close(fig)
            logger.info("Saved -> %s", path)


# Finetune-only plots

def generate_finetune_plots(ft_df, aya_df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=1.15)

    other_names = _load_other_model_names()
    has_aya = not aya_df.empty

    if has_aya:
        merged = ft_df.merge(
            aya_df[[c for c in aya_df.columns if c.startswith("aya_")] + ["lang"]],
            on="lang", how="left",
        )
    else:
        merged = ft_df.copy()

    df_sorted = merged.sort_values("lang_name")

    # Improvement heatmap FT vs Base
    col_labels = {
        "EM (En)": (df_sorted["ft_em_en"].values - df_sorted["bp_em_en"].values) * 100,
        "F1 (En)": (df_sorted["ft_f1_en"].values - df_sorted["bp_f1_en"].values) * 100,
        "SimSem (En)": (df_sorted["ft_sim_en"].values - df_sorted["bp_sim_en"].values) * 100,
        "EM (Src)": (df_sorted["ft_em_src"].values - df_sorted["bp_em_src"].values) * 100,
        "F1 (Src)": (df_sorted["ft_f1_src"].values - df_sorted["bp_f1_src"].values) * 100,
        "SimSem (Src)": (df_sorted["ft_sim_src"].values - df_sorted["bp_sim_src"].values) * 100,
    }
    delta_data = pd.DataFrame({"Language": df_sorted["lang_name"].values, **col_labels}).set_index("Language")

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.heatmap(
        delta_data, annot=True, fmt=".1f", center=0,
        cmap="RdYlGn", linewidths=0.5, ax=ax,
        cbar_kws={"label": "Improvement (pp)"},
        annot_kws={"fontsize": 11},
    )
    ft_label = other_names.get("finetuned", "Finetuned QLoRA")
    base_label = other_names.get("base_qwen", "Base Qwen2.5-3B")
    ax.set_title(
        f"{ft_label} Improvement over {base_label}\n(percentage points)",
        fontsize=13, fontweight="bold",
    )
    ax.set_ylabel("Language", fontsize=11)
    ax.set_xlabel("Metric", fontsize=11)
    fig.tight_layout()
    path = output_dir / "finetune_vs_base_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved -> %s", path)

    if has_aya:
        aya_label = other_names.get("aya", "Aya-23-8B")
        col_labels_aya = {
            "EM (En)": (df_sorted["ft_em_en"].values - df_sorted["aya_piv_em_en"].values) * 100,
            "F1 (En)": (df_sorted["ft_f1_en"].values - df_sorted["aya_piv_f1_en"].values) * 100,
            "SimSem (En)": (df_sorted["ft_sim_en"].values - df_sorted["aya_piv_sim_en"].values) * 100,
            "EM (Src)": (df_sorted["ft_em_src"].values - df_sorted["aya_dir_em_src"].values) * 100,
            "F1 (Src)": (df_sorted["ft_f1_src"].values - df_sorted["aya_dir_f1_src"].values) * 100,
            "SimSem (Src)": (df_sorted["ft_sim_src"].values - df_sorted["aya_dir_sim_src"].values) * 100,
        }
        delta_aya = pd.DataFrame({"Language": df_sorted["lang_name"].values, **col_labels_aya}).set_index("Language")

        fig, ax = plt.subplots(figsize=(11, 6))
        sns.heatmap(
            delta_aya, annot=True, fmt=".1f", center=0,
            cmap="RdYlGn", linewidths=0.5, ax=ax,
            cbar_kws={"label": "Improvement (pp)"},
            annot_kws={"fontsize": 11},
        )
        ax.set_title(
            f"{ft_label} Improvement over {aya_label}\n(percentage points)",
            fontsize=13, fontweight="bold",
        )
        ax.set_ylabel("Language", fontsize=11)
        ax.set_xlabel("Metric", fontsize=11)
        fig.tight_layout()
        path = output_dir / "finetune_vs_aya_heatmap.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved -> %s", path)


# Main

def main():
    parser = argparse.ArgumentParser(description="Analyze multilingual QA bench results.")
    parser.add_argument("--plot", action="store_true", help="Generate plots")
    parser.add_argument("--finetune", action="store_true", help="Finetune results only")
    parser.add_argument("--benchmark", action="store_true", help="Benchmark results only")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    output_dir = ROOT / "report"
    show_all = not args.finetune and not args.benchmark

    ft_df = load_finetune_results()
    aya_df = load_aya_results()
    bench_df = load_benchmark_results()
    udf = build_unified_df(ft_df, aya_df, bench_df)

    other_names = _load_other_model_names()
    ft_name = other_names.get("finetuned", "Finetuned QLoRA")

    if show_all or args.benchmark:
        if not udf.empty:
            print_unified_table(udf, "source",
                "ALL MODELS - Source-Language Evaluation (direct answers)")
            print_unified_table(udf, "english",
                "ALL MODELS - English-Side Evaluation (translate-pivot)")
            if ft_name in udf["model"].values:
                print_delta_table(udf, ft_name, "source",
                    f"IMPROVEMENT vs {ft_name} - Source Side (pp)")

    if show_all or args.finetune:
        if not ft_df.empty:
            has_aya = not aya_df.empty
            if has_aya:
                merged = ft_df.merge(
                    aya_df[[c for c in aya_df.columns if c.startswith("aya_")] + ["lang"]],
                    on="lang", how="left",
                )
                for c in [col for col in merged.columns if col.startswith("aya_")]:
                    merged[c] = merged[c].fillna(0)
            else:
                merged = ft_df

            d_sim_en = (merged["ft_sim_en"].mean() - merged["bp_sim_en"].mean()) * 100
            d_sim_src = (merged["ft_sim_src"].mean() - merged["bp_sim_src"].mean()) * 100

            base_name = other_names.get("base_qwen", "Base Qwen2.5-3B")
            aya_name = other_names.get("aya", "Aya-23-8B")

            print(_header("KEY FINDINGS"))
            print(f"  - Finetuning improves English-side SimSem by {d_sim_en:+.1f}pp over {base_name}")
            print(f"  - Finetuning improves Source-side SimSem by {d_sim_src:+.1f}pp over {base_name}")
            if has_aya:
                d_sim_en_a = (merged["ft_sim_en"].mean() - merged["aya_piv_sim_en"].mean()) * 100
                d_sim_src_a = (merged["ft_sim_src"].mean() - merged["aya_dir_sim_src"].mean()) * 100
                print(f"  - Finetuning improves English-side SimSem by {d_sim_en_a:+.1f}pp over {aya_name}")
                print(f"  - Finetuning improves Source-side SimSem by {d_sim_src_a:+.1f}pp over {aya_name}")

            if not bench_df.empty:
                ft_avg = merged["ft_sim_src"].mean()
                for model_short, group in bench_df.groupby("model_short"):
                    diff = (ft_avg - group["dir_sim_src"].mean()) * 100
                    print(f"  - {ft_name} vs {model_short}: {diff:+.1f}pp source SimSem")

            print(f"  - {len(merged)} languages evaluated, {merged['n_samples'].sum()} total test samples")
            print()

    if args.plot:
        if show_all or args.benchmark:
            if not udf.empty:
                generate_unified_plots(udf, output_dir)
        if show_all or args.finetune:
            if not ft_df.empty:
                generate_finetune_plots(ft_df, aya_df, output_dir)
        logger.info("All plots saved to %s/", output_dir)


if __name__ == "__main__":
    main()
