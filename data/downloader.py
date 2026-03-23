"""
Dataset downloader and preprocessor for AfriQA multilingual QA data.

Usage:
    python -m data.downloader              # download and process all languages
    python -m data.downloader --lang yor   # download and process Yoruba
    python -m data.downloader --lang fon --with-context  # also download gold passages
"""

import argparse
import ast
import logging
import sys
from functools import lru_cache
from pathlib import Path

# Ensure project root is on sys.path for direct execution
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from requests.exceptions import HTTPError

from paths import RAW_DIR, PROCESSED_DIR, LANGUAGES_CONFIG
from utils import load_config, load_jsonl, save_json, fetch_text


logger = logging.getLogger("mqab.data")

CONFIG_PATH = LANGUAGES_CONFIG


@lru_cache
def get_languages(config: dict | None = None) -> dict:
    """Return the languages dict from config."""
    if config is None:
        config = load_config(CONFIG_PATH)
    return config["languages"]


def get_queries_url(lang_code: str, config: dict) -> str:
    """Build the queries URL for a language."""
    base = config["base_url"]
    pivot = config["languages"][lang_code]["pivot"]
    return f"{base}/queries/{lang_code}/queries.afriqa.{lang_code}.{pivot}.train.json"


def get_passages_url(lang_code: str, config: dict) -> str:
    """Build the gold passages URL for a language."""
    base = config["base_url"]
    pivot = config["languages"][lang_code]["pivot"]
    filename = f"gold_span_passages.afriqa.{lang_code}.{pivot}.train.json"
    return f"{base}/gold_passages/{lang_code}/{filename}"


def download(lang_code: str, config: dict | None = None) -> Path:
    """Download the raw dataset for a language and return the saved path."""
    if config is None:
        config = load_config(CONFIG_PATH)
    lang = config["languages"][lang_code]
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    url = get_queries_url(lang_code, config)
    raw_path = RAW_DIR / f"{lang['name']}_raw.jsonl"

    logger.info("Downloading %s dataset...", lang["name"])
    raw_path.write_text(fetch_text(url), encoding="utf-8")
    logger.info("Saved raw data -> %s", raw_path)
    return raw_path


def download_passages(lang_code: str, config: dict | None = None) -> Path:
    """Download gold passage JSON for a language and return the saved path."""
    if config is None:
        config = load_config(CONFIG_PATH)
    lang = config["languages"][lang_code]
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    url = get_passages_url(lang_code, config)
    raw_path = RAW_DIR / f"{lang['name']}_passages.json"

    logger.info("Downloading %s gold passages from %s...", lang["name"], url)
    try:
        raw_path.write_text(fetch_text(url), encoding="utf-8")
    except HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            logger.warning("Gold passages not available for %s (404), skipping", lang["name"])
            return None
        raise
    logger.info("Saved passages -> %s", raw_path)
    return raw_path

# Processing functions


def filter_queries(data: list[dict], config: dict) -> list[dict]:
    """Filter raw query data based on thresholds from config."""
    min_q = config.get("min_question_length") or None
    min_a = config.get("min_answer_length") or None

    filtered = []
    for item in data:
        question = item.get("question", "")
        answers_raw = item.get("answers", "[]")

        try:
            answers = ast.literal_eval(answers_raw)
        except (ValueError, SyntaxError):
            continue

        if not answers:
            continue

        answer = answers[0]

        if len(question) < min_q:
            continue
        if len(str(answer)) < min_a:
            continue

        filtered.append({
            "question": question,
            "translated_question": item.get("translated_question", ""),
            "answer": answer,
        })

    return filtered


def filter_passages(data: list[dict], config: dict) -> list[dict]:
    """Filter gold passage data based on thresholds from config."""
    min_q = config.get("min_question_length") or None
    min_a = config.get("min_answer_length") or None
    min_c = config.get("min_context_length") or None

    filtered = []
    for item in data:
        context = item.get("context") or ""
        question = item.get("question_lang") or ""
        answer = item.get("answer_lang") or ""
        translated_question = item.get("question_translated") or ""

        if len(context.strip()) < min_c:
            continue
        if len(question.strip()) < min_q:
            continue
        if len(str(answer).strip()) < min_a:
            continue

        filtered.append({
            "id": item.get("id") or "",
            "question": question,
            "translated_question": translated_question,
            "context": context,
            "answer": answer,
        })

    return filtered


def process(lang_code: str, config: dict | None = None) -> Path:
    """Filter the raw dataset and save processed output."""
    if config is None:
        config = load_config(CONFIG_PATH)
    lang = config["languages"][lang_code]
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / f"{lang['name']}_raw.jsonl"
    processed_path = PROCESSED_DIR / f"{lang['name']}_filtered.json"

    data = load_jsonl(raw_path)
    logger.info("Filtering %s dataset (%d raw samples)...", lang["name"], len(data))

    filtered = filter_queries(data, config)
    logger.info("Kept %d / %d samples", len(filtered), len(data))

    save_json(filtered, processed_path)
    logger.info("Saved processed data -> %s", processed_path)
    return processed_path


def process_with_context(lang_code: str, config: dict | None = None) -> Path:
    """Process gold passages into (context, question, answer) triples."""
    if config is None:
        config = load_config(CONFIG_PATH)
    lang = config["languages"][lang_code]
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / f"{lang['name']}_passages.json"
    output_path = PROCESSED_DIR / f"{lang['name']}_with_context.json"

    passages = load_jsonl(raw_path)
    logger.info("Processing %d gold passages for %s...", len(passages), lang["name"])

    filtered = filter_passages(passages, config)
    logger.info("Kept %d / %d samples with context", len(filtered), len(passages))

    save_json(filtered, output_path)
    logger.info("Saved -> %s", output_path)
    return output_path


# Logic


def run(lang_code: str, with_context: bool = False):
    """Download and process a single language dataset."""
    config = load_config(CONFIG_PATH)
    download(lang_code, config)
    process(lang_code, config)
    if with_context:
        passages_path = download_passages(lang_code, config)
        if passages_path is not None:
            process_with_context(lang_code, config)


def run_all(with_context: bool = False):
    """Download and process all language datasets."""
    config = load_config(CONFIG_PATH)
    for lang_code in sorted(config["languages"].keys()):
        try:
            run(lang_code, with_context=with_context)
        except Exception:
            logger.exception("Failed to download/process %s, skipping", lang_code)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s │ %(name)s │ %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Download and preprocess AfriQA data.")
    parser.add_argument(
        "--lang", default=None, choices=sorted(get_languages().keys()),
        help="Language code (default: all)",
    )
    parser.add_argument(
        "--with-context", action="store_true",
        help="Also download gold passages and build context-enriched data",
    )
    args = parser.parse_args()

    if args.lang:
        run(args.lang, with_context=args.with_context)
    else:
        run_all(with_context=args.with_context)
