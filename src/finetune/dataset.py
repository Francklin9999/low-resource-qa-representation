"""
Training dataset builder: mix data sources, create round-trip augmentation,
and format as instruction-tuning prompts for QLoRA fine-tuning.
"""

import json
import logging
import random

from paths import TRAINING_DIR
from src.translate import translate_batch
from utils import save_jsonl
from utils.prompts import QA_PROMPT_TEMPLATE

logger = logging.getLogger("mqab.finetune.dataset")


def format_prompt(context: str, question: str) -> str:
    """Format a (context, question) pair into the instruction prompt."""
    return QA_PROMPT_TEMPLATE.format(context=context.strip(), question=question.strip())


def create_round_trip_augmented(
    english_samples: list[dict],
    lang: str,
    max_samples: int | None = None,
    seed: int = 42,
    batch_size: int = 8,
) -> list[dict]:
    """Create noisy English via round-trip translation: English -> target language -> English.

    This teaches the model robustness to translation artifacts.
    """
    rng = random.Random(seed)
    pool = english_samples.copy()
    rng.shuffle(pool)
    if max_samples:
        pool = pool[:max_samples]

    logger.info("Creating round-trip augmented data (%d samples, lang=%s)...", len(pool), lang)

    contexts_en = [s["context_en"] for s in pool]
    questions_en = [s["question_en"] for s in pool]
    answers_en = [s["answer_en"] for s in pool]

    # English -> target language (introduces translation noise)
    contexts_tgt = translate_batch(contexts_en, src_lang="en", tgt_lang=lang, batch_size=batch_size)
    questions_tgt = translate_batch(questions_en, src_lang="en", tgt_lang=lang, batch_size=batch_size)
    answers_tgt = translate_batch(answers_en, src_lang="en", tgt_lang=lang, batch_size=batch_size)

    # Target language -> English (creates noisy English)
    contexts_rt = translate_batch(contexts_tgt, src_lang=lang, tgt_lang="en", batch_size=batch_size)
    questions_rt = translate_batch(questions_tgt, src_lang=lang, tgt_lang="en", batch_size=batch_size)
    answers_rt = translate_batch(answers_tgt, src_lang=lang, tgt_lang="en", batch_size=batch_size)

    augmented = []
    for i in range(len(pool)):
        # Skip if round-trip destroyed the answer
        if len(answers_rt[i].strip()) < 1:
            continue
        augmented.append({
            "context_en": contexts_rt[i],
            "question_en": questions_rt[i],
            "answer_en": answers_rt[i],
            "origin": "round_trip_augmented",
        })

    logger.info("Round-trip augmentation produced %d samples", len(augmented))
    return augmented


def build_training_mix(
    translated: list[dict],
    english_qa: list[dict],
    augmented: list[dict],
    translated_ratio: float,
    english_ratio: float,
    augmented_ratio: float,
    seed: int,
) -> list[dict]:
    """Mix three data buckets according to target ratios.

    Bucket 1 (translated): 60-70% - translated target language QA (main bucket)
    Bucket 2 (english_qa): 20-30% - clean English QA
    Bucket 3 (augmented): 10-20% - round-trip noisy English

    Returns shuffled mixed list.
    """
    rng = random.Random(seed)

    # Use all translated data as the anchor, then sample from English and augmented to meet ratios
    n_translated = len(translated)

    # Calculate total based on translated data being the anchor
    total_target = int(n_translated / translated_ratio)
    n_english = min(int(total_target * english_ratio), len(english_qa))
    n_augmented = min(int(total_target * augmented_ratio), len(augmented))

    # Sample
    english_sample = rng.sample(english_qa, min(n_english, len(english_qa)))
    augmented_sample = rng.sample(augmented, min(n_augmented, len(augmented)))

    # Tag origins
    for s in translated:
        s.setdefault("origin", "translated")
    for s in english_sample:
        s.setdefault("origin", "squad_english")
    for s in augmented_sample:
        s.setdefault("origin", "round_trip_augmented")

    mixed = translated + english_sample + augmented_sample
    rng.shuffle(mixed)

    logger.info(
        "Training mix: %d translated + %d english + %d augmented = %d total",
        len(translated), len(english_sample), len(augmented_sample), len(mixed),
    )
    return mixed


def format_for_training(samples: list[dict]) -> list[dict]:
    """Convert samples into instruction-tuning format: {id, prompt, target, origin}.

    Each sample must have context_en, question_en, answer_en.
    """
    formatted = []
    for i, sample in enumerate(samples):
        prompt = format_prompt(
            context=sample["context_en"],
            question=sample["question_en"],
        )
        formatted.append({
            "id": sample.get("id", f"train_{i:05d}"),
            "prompt": prompt,
            "target": sample["answer_en"].strip(),
            "origin": sample.get("origin", "unknown"),
        })
    return formatted


def build_training_data(
    lang: str,
    translated_ratio: float,
    english_ratio: float,
    augmented_ratio: float,
    augmented_max: int,
    seed: int,
) -> dict:
    """Full dataset building pipeline for a given language.

    Expects prepare.py to have already run (splits and english_qa saved).

    1. Load train/val splits (already translated to English)
    2. Load English QA data
    3. Create round-trip augmented data
    4. Mix according to ratios
    5. Format as instruction prompts
    6. Save as JSONL

    Returns dict with paths and statistics.
    """
    lang_dir = TRAINING_DIR / lang
    splits_dir = lang_dir / "splits"

    # Load language splits
    with open(splits_dir / f"{lang}_train.json", "r", encoding="utf-8") as f:
        lang_train = json.load(f)
    with open(splits_dir / f"{lang}_val.json", "r", encoding="utf-8") as f:
        lang_val = json.load(f)

    # Load English QA (shared across languages)
    with open(TRAINING_DIR / "english_qa.json", "r", encoding="utf-8") as f:
        english_qa = json.load(f)

    # Create round-trip augmented data from English samples
    augmented = create_round_trip_augmented(
        english_qa, lang=lang, max_samples=augmented_max, seed=seed
    )

    # Mix training data
    train_mixed = build_training_mix(
        translated=lang_train,
        english_qa=english_qa,
        augmented=augmented,
        translated_ratio=translated_ratio,
        english_ratio=english_ratio,
        augmented_ratio=augmented_ratio,
        seed=seed,
    )

    # Format as instruction prompts
    train_formatted = format_for_training(train_mixed)
    val_formatted = format_for_training(lang_val)

    # Save
    train_path = save_jsonl(train_formatted, lang_dir / "train.jsonl")
    val_path = save_jsonl(val_formatted, lang_dir / "val.jsonl")

    stats = {
        "lang": lang,
        "train_total": len(train_formatted),
        "train_translated": len(lang_train),
        "train_english": len([s for s in train_mixed if s.get("origin") == "squad_english"]),
        "train_augmented": len([s for s in train_mixed if s.get("origin") == "round_trip_augmented"]),
        "val_total": len(val_formatted),
        "train_path": str(train_path),
        "val_path": str(val_path),
    }
    logger.info("Dataset build complete for %s: %s", lang, stats)
    return stats
