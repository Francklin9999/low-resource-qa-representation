"""GPU memory management for fine-tuning pipelines."""

import gc
import logging

import torch

from src import translate as translate_mod
from src import evaluate as evaluate_mod

logger = logging.getLogger("mqab.finetune.gpu")


def free_gpu_memory():
    """Free cached models (NLLB, LaBSE) from memory and clear CUDA cache."""
    # Clear NLLB translation model
    if translate_mod._model is not None:
        translate_mod._model.cpu()
        translate_mod._model = None
        translate_mod._tokenizer = None

    # Clear LaBSE embedding model
    if evaluate_mod._embedder is not None:
        evaluate_mod._embedder = None

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    logger.info("Freed GPU memory for training.")
