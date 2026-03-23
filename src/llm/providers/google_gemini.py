import os

from google import genai

from src.llm.base import LLMProvider
from src.llm.registry import register


@register("gemini")
class GeminiProvider(LLMProvider):
    """Google Gemini API provider (Gemini 2.5 Pro)."""

    def __init__(self, model: str = "gemini-2.5-pro", **kwargs):
        super().__init__(model)
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def ask(self, question: str, system_prompt: str = "") -> str:
        config = genai.types.GenerateContentConfig(temperature=0)
        if system_prompt:
            config.system_instruction = system_prompt

        response = self.client.models.generate_content(
            model=self.model,
            contents=question,
            config=config,
        )
        return response.text
