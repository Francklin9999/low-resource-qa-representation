import os

from openai import OpenAI

from src.llm.base import LLMProvider
from src.llm.registry import register


@register("openai")
class OpenAIProvider(LLMProvider):
    """OpenAI API provider (GPT-5.3)."""

    def __init__(self, model: str = "gpt-5.3-chat-latest", **kwargs):
        super().__init__(model)
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def ask(self, question: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
