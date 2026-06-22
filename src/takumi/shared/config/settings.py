from enum import StrEnum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: LLMProvider = LLMProvider.OPENAI
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    openai_model: str = "gpt-4o"
    anthropic_model: str = "claude-sonnet-4-20250514"
    log_level: str = "INFO"

    @field_validator("llm_provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: str | LLMProvider) -> LLMProvider:
        if isinstance(value, LLMProvider):
            return value
        return LLMProvider(value.strip().lower())

    def validate_api_key(self) -> None:
        if self.llm_provider == LLMProvider.OPENAI and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if self.llm_provider == LLMProvider.ANTHROPIC and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")

    def masked_config(self) -> dict[str, str]:
        return {
            "llm_provider": self.llm_provider.value,
            "openai_model": self.openai_model,
            "anthropic_model": self.anthropic_model,
            "openai_api_key": self._mask(self.openai_api_key),
            "anthropic_api_key": self._mask(self.anthropic_api_key),
            "log_level": self.log_level,
        }

    @staticmethod
    def _mask(value: str) -> str:
        if not value:
            return "(not set)"
        if len(value) <= 8:
            return "***"
        return f"{value[:4]}...{value[-4:]}"


def get_settings() -> Settings:
    return Settings()
