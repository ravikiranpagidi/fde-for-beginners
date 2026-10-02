import os

from fde_beginners.ai.mock_provider import MockLLMProvider
from fde_beginners.ai.provider import LLMProvider


class UnsupportedProvider(ValueError):
    pass


def create_provider(name: str | None = None) -> LLMProvider:
    selected = os.environ.get("FDE_LLM_PROVIDER", "mock") if name is None else name
    if selected != "mock":
        raise UnsupportedProvider(f"Unsupported provider {selected!r}; available: mock")
    return MockLLMProvider()
