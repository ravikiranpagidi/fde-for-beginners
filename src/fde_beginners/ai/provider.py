from typing import Protocol

from fde_beginners.ai.models import LLMRequest, LLMResponse


class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Return validated application data, never vendor SDK objects."""
        ...
