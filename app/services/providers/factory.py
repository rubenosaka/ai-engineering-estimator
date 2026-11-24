from app.config import Settings
from app.services.llm import LanguageModel, LanguageModelError
from app.services.providers.anthropic import AnthropicLanguageModel
from app.services.providers.openai import OpenAILanguageModel


def build_language_model(settings: Settings) -> LanguageModel:
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise LanguageModelError("LLM provider is not configured")
        return OpenAILanguageModel(api_key=settings.OPENAI_API_KEY, model=settings.LLM_MODEL)
    if not settings.ANTHROPIC_API_KEY:
        raise LanguageModelError("LLM provider is not configured")
    return AnthropicLanguageModel(api_key=settings.ANTHROPIC_API_KEY, model=settings.LLM_MODEL)
