import pytest

from app.config import Settings
from app.services.llm import ChatMessage, LanguageModelError
from app.services.providers.factory import build_language_model
from app.services.providers.messages import to_anthropic_messages, to_openai_messages


def test_openai_messages_keep_system_and_user() -> None:
    messages = [
        ChatMessage(role="system", content="rol"),
        ChatMessage(role="user", content="reunión"),
    ]

    assert to_openai_messages(messages) == [
        {"role": "system", "content": "rol"},
        {"role": "user", "content": "reunión"},
    ]


def test_anthropic_messages_split_the_system_prompt() -> None:
    messages = [
        ChatMessage(role="system", content="rol"),
        ChatMessage(role="user", content="reunión"),
    ]

    system, dialogue = to_anthropic_messages(messages)

    assert system == "rol"
    assert dialogue == [{"role": "user", "content": "reunión"}]


def test_factory_requires_the_selected_provider_key() -> None:
    settings = Settings.model_construct(
        OPENAI_API_KEY=None,
        ANTHROPIC_API_KEY="present",
        LLM_PROVIDER="openai",
        LLM_MODEL="gpt-4o-mini",
        APP_ENV="development",
        LOG_LEVEL="DEBUG",
    )

    with pytest.raises(LanguageModelError):
        build_language_model(settings)
