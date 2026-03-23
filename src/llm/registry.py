from src.llm.base import LLMProvider

_PROVIDERS: dict[str, type[LLMProvider]] = {}


def register(name: str):
    """Decorator to register an LLM provider."""
    def decorator(cls: type[LLMProvider]):
        _PROVIDERS[name] = cls
        return cls
    return decorator


def get_provider(name: str, model: str, **kwargs) -> LLMProvider:
    """Get a provider instance by name."""
    if name not in _PROVIDERS:
        raise ValueError(
            f"Unknown provider {name!r}. Available: {list(_PROVIDERS.keys())}"
        )
    return _PROVIDERS[name](model=model, **kwargs)


def list_providers() -> list[str]:
    """Return all registered provider names."""
    return list(_PROVIDERS.keys())
