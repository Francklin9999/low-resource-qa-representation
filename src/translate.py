import logging

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from paths import MODELS_CONFIG
from utils import load_config

logger = logging.getLogger("mqab.translate")

_models_cfg = load_config(MODELS_CONFIG)
_translation_cfg = _models_cfg["translation"]

MODEL_NAME = _translation_cfg["model"]
LANG_CODES = _translation_cfg["lang_codes"]
_device = _translation_cfg["device"]

_model = None
_tokenizer = None


def _load_model():
    global _model, _tokenizer
    if _model is None:
        logger.info("Loading NLLB model (%s) on %s...", MODEL_NAME, _device)
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(_device)
    return _model, _tokenizer


def translate(text: str, src_lang: str, tgt_lang: str) -> str:
    """Translate text between languages.

    Args:
        text: Input text.
        src_lang: Source language code (e.g. "hau", "en").
        tgt_lang: Target language code (e.g. "en", "hau").
    """
    model, tokenizer = _load_model()

    src_code = LANG_CODES[src_lang]
    tgt_code = LANG_CODES[tgt_lang]

    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(_device)

    tgt_lang_id = tokenizer.convert_tokens_to_ids(tgt_code)
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tgt_lang_id,
        max_new_tokens=512,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def translate_batch(
    texts: list[str],
    src_lang: str,
    tgt_lang: str,
    batch_size: int = 16,
) -> list[str]:
    """Translate a list of texts in batches."""
    model, tokenizer = _load_model()

    src_code = LANG_CODES[src_lang]
    tgt_code = LANG_CODES[tgt_lang]
    tgt_lang_id = tokenizer.convert_tokens_to_ids(tgt_code)

    results = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        tokenizer.src_lang = src_code
        inputs = tokenizer(batch, return_tensors="pt", truncation=True, padding=True).to(_device)
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tgt_lang_id,
            max_new_tokens=512,
        )
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        results.extend(decoded)

    return results
