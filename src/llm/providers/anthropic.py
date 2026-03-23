import os

import anthropic

from src.llm.base import LLMProvider
from src.llm.registry import register


@register("anthropic")
class AnthropicProvider(LLMProvider):
    """Anthropic API provider (Claude Opus 4.5)."""

    def __init__(self, model: str = "claude-opus-4-5-20251101", **kwargs):
        super().__init__(model)
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def ask(self, question: str, system_prompt: str = "") -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 1024,
            "temperature": 0,
            "messages": [{"role": "user", "content": question}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text


@register("anthropic-thinking")
class AnthropicThinkingProvider(LLMProvider):
    """Anthropic with extended thinking (Claude Sonnet 4.5)."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929", **kwargs):
        super().__init__(model)
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def ask(self, question: str, system_prompt: str = "") -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 16000,
            "thinking": {"type": "enabled", "budget_tokens": 10000},
            "messages": [{"role": "user", "content": question}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        for block in response.content:
            if block.type == "text":
                return block.text
        return ""
