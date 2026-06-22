from langchain_core.language_models.chat_models import BaseChatModel

from takumi.shared.config.settings import LLMProvider, Settings


def get_llm(settings: Settings) -> BaseChatModel:
    settings.validate_api_key()

    if settings.llm_provider == LLMProvider.OPENAI:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    if settings.llm_provider == LLMProvider.ANTHROPIC:
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            api_key=settings.anthropic_api_key,
            model_name=settings.anthropic_model,
        )

    if settings.llm_provider == LLMProvider.OLLAMA:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
