from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base class for all LLM providers."""

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def ask(self, question: str, system_prompt: str = "") -> str:
        """Send a question and return the raw text response."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r})"
