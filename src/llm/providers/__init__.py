# Import all providers so they self-register
from src.llm.providers import anthropic, openai, google_gemini, local_mt5

__all__ = ["anthropic", "openai", "google_gemini", "local_mt5"]
