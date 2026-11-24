from pydantic import BaseModel

from app.context.examples import ESTIMATION_EXAMPLES
from app.services.llm import ChatMessage, Completion, LanguageModel, TokenUsage
from app.services.prompt import build_system_prompt


class Estimation(BaseModel):
    estimation: str
    model: str
    provider: str
    usage: TokenUsage


def generate_estimation(transcription: str, language_model: LanguageModel) -> Estimation:
    messages = [
        ChatMessage(role="system", content=build_system_prompt(ESTIMATION_EXAMPLES)),
        ChatMessage(role="user", content=transcription),
    ]
    completion: Completion = language_model.complete(messages)
    return Estimation(
        estimation=completion.content,
        model=completion.model,
        provider=completion.provider,
        usage=completion.usage,
    )
