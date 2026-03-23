import logging
import re
import string

import numpy as np
from sentence_transformers import SentenceTransformer
from paths import MODELS_CONFIG
from utils import load_config

logger = logging.getLogger("mqab.evaluate")

_models_cfg = load_config(MODELS_CONFIG)
_embedder = None
_device = _models_cfg["evaluation"]["device"]
MODEL_NAME = _models_cfg["evaluation"]["model"]


def _load_embedder():
    global _embedder
    if _embedder is None:
        logger.info("Loading embedding model (%s) on %s...", MODEL_NAME, _device)
        _embedder = SentenceTransformer(MODEL_NAME, device=_device)
    return _embedder


def normalize(text: str) -> str:
    """Lowercase, strip punctuation and extra whitespace."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def exact_match(predicted: str, gold: str) -> float:
    """Returns 1.0 if normalized strings match, else 0.0."""
    return float(normalize(predicted) == normalize(gold))


def f1_score(predicted: str, gold: str) -> float:
    """Token-level F1 (SQuAD-style)."""
    pred_tokens = normalize(predicted).split()
    gold_tokens = normalize(gold).split()

    if not gold_tokens:
        return float(not pred_tokens)
    if not pred_tokens:
        return 0.0

    common = set(pred_tokens) & set(gold_tokens)
    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def semantic_similarity(predicted: str, gold: str) -> float:
    """Cosine similarity using embeddings."""
    embedder = _load_embedder()
    embeddings = embedder.encode([predicted, gold], normalize_embeddings=True)
    return float(np.dot(embeddings[0], embeddings[1]))


def evaluate(predicted: str, gold: str) -> dict:
    """Run all evaluation metrics."""
    return {
        "exact_match": exact_match(predicted, gold),                   # 1 if strings match exactly, else 0
        "f1": f1_score(predicted, gold),                               # token-level overlap (harmonic mean of precision & recall)
        "semantic_similarity": semantic_similarity(predicted, gold),   # cosine similarity via LaBSE embeddings
    }
