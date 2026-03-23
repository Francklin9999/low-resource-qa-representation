import logging

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.llm.base import LLMProvider
from src.llm.registry import register

logger = logging.getLogger("mqab.llm.mt5")

_model = None
_tokenizer = None


def _load_mt5(model_name: str):
    """Load mT5 model and tokenizer (cached globally)."""
    global _model, _tokenizer
    if _model is not None:
        return

    logger.info("Loading mT5 model: %s ...", model_name)
    _tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    _model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if not torch.cuda.is_available():
        _model = _model.to("cpu")
    _model.eval()
    logger.info("mT5 model loaded on %s", next(_model.parameters()).device)


@register("mt5")
class MT5Provider(LLMProvider):
    """Local mT5 model (encoder-decoder seq2seq for multilingual QA).

    mT5 expects input formatted as: "question: <question> context: <context>"
    The system_prompt is prepended to give task instructions.
    """

    def __init__(self, model: str = "google/mt5-large", **kwargs):
        super().__init__(model)
        _load_mt5(model)

    def ask(self, question: str, system_prompt: str = "") -> str:
        input_text = question
        if system_prompt:
            input_text = f"{system_prompt}\n{question}"

        inputs = _tokenizer(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
        ).to(next(_model.parameters()).device)

        with torch.no_grad():
            outputs = _model.generate(
                **inputs,
                max_new_tokens=128,
                num_beams=4,
                early_stopping=True,
            )

        return _tokenizer.decode(outputs[0], skip_special_tokens=True)
