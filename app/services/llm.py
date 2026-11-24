from typing import Literal, Protocol

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user"]
    content: str


class TokenUsage(BaseModel):
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)


class Completion(BaseModel):
    content: str
    model: str
    provider: str
    usage: TokenUsage


class LanguageModel(Protocol):
    def complete(self, messages: list[ChatMessage]) -> Completion: ...


class LanguageModelError(Exception):
    pass
