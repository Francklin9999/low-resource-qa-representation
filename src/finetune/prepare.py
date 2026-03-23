"""
Data preparation for fine-tuning: load AfriQA data with context,
create train/val/test splits, translation, validate quality.
"""

import json
import logging
import random
from pathlib import Path

from src.evaluate import semantic_similarity
from src.translate import translate_batch
from data.downloader import get_languages
from datasets import load_dataset
from paths import DATA_DIR, PROCESSED_DIR, TRAINING_DIR

LANGUAGES = get_languages()

logger = logging.getLogger("mqab.finetune.prepare")


def load_data_with_context(lang: str) -> list[dict]:
    """Load the context-enriched dataset for a given language."""
    lang_name = LANGUAGES[lang]["name"]
    path = PROCESSED_DIR / f"{lang_name}_with_context.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: python -m data.downloader --lang {lang} --with-context"
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_data(
    data: list[dict],
    train_ratio: float = 0.70,
    val_ratio: float = 0.10,
    seed: int = 42,
) -> dict[str, list[dict]]:
    """Split data into train/val/test sets with deterministic shuffle.

    Returns dict with keys: "train", "val", "test".
    """
    rng = random.Random(seed)
    shuffled = data.copy()
    rng.shuffle(shuffled)

    n = len(shuffled)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    return {
        "train": shuffled[:train_end],
        "val": shuffled[train_end:val_end],
        "test": shuffled[val_end:],
    }


def translate_to_english(
    samples: list[dict],
    lang: str,
    batch_size: int = 8,
) -> list[dict]:
    """Translate context, question, and answer to English.

    For languages with pivot=fr and human French translations available,
    uses a two-hop strategy: source->French (human) then French->English (NLLB).
    Otherwise falls back to direct source->English.

    Returns new list with added *_en fields.
    """
    pivot = LANGUAGES[lang].get("pivot", "en")

    logger.info("Translating %d %s samples to English...", len(samples), lang)

    contexts = [s["context"] for s in samples]
    questions = [s["question"] for s in samples]
    answers = [str(s["answer"]) for s in samples]

    # Check if human pivot translations exist for questions
    has_pivot_translations = all(s.get("translated_question") for s in samples)

    if has_pivot_translations and pivot != "en":
        logger.info("Using two-hop: %s questions have human %s -> translating %s->English", lang, pivot, pivot)
        questions_pivot = [s["translated_question"] for s in samples]
        questions_en = translate_batch(questions_pivot, src_lang=pivot, tgt_lang="en", batch_size=batch_size)
    elif has_pivot_translations and pivot == "en":
        logger.info("Using human English translations for questions")
        questions_en = [s["translated_question"] for s in samples]
    else:
        questions_en = translate_batch(questions, src_lang=lang, tgt_lang="en", batch_size=batch_size)

    # Context and answers: always source -> English
    contexts_en = translate_batch(contexts, src_lang=lang, tgt_lang="en", batch_size=batch_size)
    answers_en = translate_batch(answers, src_lang=lang, tgt_lang="en", batch_size=batch_size)

    translated = []
    for i, sample in enumerate(samples):
        translated.append({
            **sample,
            "context_en": contexts_en[i],
            "question_en": questions_en[i],
            "answer_en": answers_en[i],
        })

    logger.info("Translation complete: %d samples", len(translated))
    return translated


def validate_translations(
    samples: list[dict],
    min_answer_len: int = 1,
    min_similarity: float = 0.3,
) -> tuple[list[dict], list[dict]]:
    """Validate translation quality. Returns (good_samples, discarded_samples).

    Checks:
    - English answer is not empty
    - English context is not empty
    - Semantic similarity between original answer and English answer is above threshold
    """
    good, discarded = [], []

    for sample in samples:
        answer_en = sample.get("answer_en", "").strip()
        context_en = sample.get("context_en", "").strip()

        # Basic checks
        if len(answer_en) < min_answer_len or len(context_en) < 10:
            sample["discard_reason"] = "empty_translation"
            discarded.append(sample)
            continue

        # Semantic similarity between original answer and translated answer
        sim = semantic_similarity(str(sample["answer"]), answer_en)
        sample["translation_quality"] = round(sim, 4)

        if sim < min_similarity:
            sample["discard_reason"] = f"low_similarity={sim:.3f}"
            discarded.append(sample)
            continue

        good.append(sample)

    logger.info(
        "Validation: %d good, %d discarded (of %d total)",
        len(good), len(discarded), len(samples),
    )
    return good, discarded


def download_english_qa(source: str, max_samples: int) -> list[dict]:
    """Download clean English QA data (SQuAD or TyDi QA).

    Returns list of {"context_en", "question_en", "answer_en", "origin"} dicts.
    """

    if source == "squad":
        logger.info("Loading SQuAD v2 English QA data (max %d)...", max_samples)
        ds = load_dataset("rajpurkar/squad_v2", split="train")

        samples = []
        for item in ds:
            answers = item.get("answers", {})
            answer_texts = answers.get("text", [])
            if not answer_texts:
                continue
            context = item.get("context", "")
            question = item.get("question", "")
            if len(context) < 20 or len(question) < 10:
                continue
            samples.append({
                "context_en": context,
                "question_en": question,
                "answer_en": answer_texts[0],
                "origin": "squad_english",
            })
            if len(samples) >= max_samples:
                break

    elif source == "tydiqa":
        logger.info("Loading TyDi QA English data (max %d)...", max_samples)
        ds = load_dataset("google-research-datasets/tydiqa", "secondary_task", split="train")

        samples = []
        for item in ds:
            if item.get("id", "").startswith("english"):
                answers = item.get("answers", {})
                answer_texts = answers.get("text", [])
                if not answer_texts:
                    continue
                samples.append({
                    "context_en": item["context"],
                    "question_en": item["question"],
                    "answer_en": answer_texts[0],
                    "origin": "tydiqa_english",
                })
                if len(samples) >= max_samples:
                    break
    else:
        raise ValueError(f"Unknown English QA source: {source!r}. Use 'squad' or 'tydiqa'.")

    logger.info("Loaded %d English QA samples from %s", len(samples), source)
    return samples


def save_splits(splits: dict[str, list[dict]], lang: str, output_dir: Path | None = None) -> Path:
    """Save train/val/test splits as JSON files."""
    out = output_dir or TRAINING_DIR / lang / "splits"
    out.mkdir(parents=True, exist_ok=True)

    for name, data in splits.items():
        path = out / f"{lang}_{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Saved %s split (%d samples) -> %s", name, len(data), path)

    return out


def prepare_all(
    lang: str,
    english_source: str,
    english_max: int,
    min_similarity: float,
    seed: int,
) -> dict:
    """Full data preparation pipeline for a given language.

    1. Load data with context
    2. Split into train/val/test
    3. Translate to English
    4. Validate translation quality
    5. Download English QA data (shared, only downloaded once)
    6. Save everything

    Returns dict with paths and statistics.
    """
    lang_dir = TRAINING_DIR / lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load data
    logger.info("Step 1: Loading %s data with context...", lang)
    data = load_data_with_context(lang)
    logger.info("Loaded %d %s samples with context", len(data), lang)

    # Step 2: Split
    logger.info("Step 2: Splitting data...")
    splits = split_data(data, seed=seed)
    for name, d in splits.items():
        logger.info("  %s: %d samples", name, len(d))

    # Step 3: Translate to English
    logger.info("Step 3: Translating %s -> English...", lang)
    splits["train"] = translate_to_english(splits["train"], lang=lang)
    splits["val"] = translate_to_english(splits["val"], lang=lang)
    splits["test"] = translate_to_english(splits["test"], lang=lang)

    # Step 4: Validate translations (train and val only, test stays intact)
    logger.info("Step 4: Validating translation quality...")
    splits["train"], discarded_train = validate_translations(
        splits["train"], min_similarity=min_similarity
    )
    splits["val"], discarded_val = validate_translations(
        splits["val"], min_similarity=min_similarity
    )

    # Step 5: Download English QA (shared across languages)
    english_path = TRAINING_DIR / "english_qa.json"
    if not english_path.exists():
        logger.info("Step 5: Downloading English QA data...")
        english_qa = download_english_qa(source=english_source, max_samples=english_max)
        with open(english_path, "w", encoding="utf-8") as f:
            json.dump(english_qa, f, ensure_ascii=False, indent=2)
    else:
        logger.info("Step 5: English QA data already exists, skipping download.")

    # Step 6: Save splits
    logger.info("Step 6: Saving all splits...")
    splits_dir = save_splits(splits, lang=lang)

    # Save discarded for inspection
    discarded_path = lang_dir / "discarded.json"
    with open(discarded_path, "w", encoding="utf-8") as f:
        json.dump(discarded_train + discarded_val, f, ensure_ascii=False, indent=2)

    stats = {
        "lang": lang,
        "total": len(data),
        "train": len(splits["train"]),
        "val": len(splits["val"]),
        "test": len(splits["test"]),
        "discarded": len(discarded_train) + len(discarded_val),
        "splits_dir": str(splits_dir),
    }
    logger.info("Preparation complete for %s: %s", lang, stats)
    return stats
