from anthropic import Anthropic, AnthropicError

from app.services.llm import ChatMessage, Completion, LanguageModelError, TokenUsage
from app.services.providers.messages import to_anthropic_messages

MAX_TOKENS = 4000


class AnthropicLanguageModel:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def complete(self, messages: list[ChatMessage]) -> Completion:
        system, dialogue = to_anthropic_messages(messages)
        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=dialogue,
            )
        except AnthropicError as exc:
            raise LanguageModelError(type(exc).__name__) from None

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        return Completion(
            content=response.content[0].text,
            model=response.model,
            provider="anthropic",
            usage=TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
        )
