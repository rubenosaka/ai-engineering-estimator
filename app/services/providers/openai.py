from openai import OpenAI, OpenAIError

from app.services.llm import ChatMessage, Completion, LanguageModelError, TokenUsage
from app.services.providers.messages import to_openai_messages

MAX_TOKENS = 4000


class OpenAILanguageModel:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def complete(self, messages: list[ChatMessage]) -> Completion:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=to_openai_messages(messages),
                max_tokens=MAX_TOKENS,
            )
        except OpenAIError as exc:
            raise LanguageModelError(type(exc).__name__) from None

        usage = response.usage
        content = response.choices[0].message.content or ""
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0
        return Completion(
            content=content,
            model=response.model,
            provider="openai",
            usage=TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
        )
