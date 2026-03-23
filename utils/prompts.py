"""Prompt constants loaded from configs/prompts.yaml."""

from paths import PROMPTS_CONFIG
from utils import load_config

_prompts_cfg = load_config(PROMPTS_CONFIG)

SYSTEM_PROMPT = _prompts_cfg["system_prompt"]
CONTEXT_SYSTEM_PROMPT = _prompts_cfg["context_system_prompt"]
FINETUNE_SYSTEM_PROMPT = _prompts_cfg["finetune_system_prompt"]
QA_PROMPT_TEMPLATE = _prompts_cfg["qa_prompt_template"]
