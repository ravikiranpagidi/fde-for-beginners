from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ContextRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    source_id: str
    text: str


class LLMRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    user_input: str = Field(min_length=1)
    system_instructions: str = ""
    context: tuple[ContextRecord, ...] = ()


class LLMResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    answer: str
    citations: tuple[str, ...] = ()
    support: Literal["extractive", "insufficient"]
    provider: str = "mock"
    request_digest: str
    structured_content: dict[str, str] | None = None
