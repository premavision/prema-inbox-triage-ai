"""Application settings and configuration helpers."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = "Inbox Triage AI"
    app_env: str = Field(default="local", alias="APP_ENV")
    database_url: str = Field(default="sqlite:///./inbox.db", alias="DATABASE_URL")

    # Provider toggles
    gmail_enabled: bool = Field(default=True, alias="GMAIL_ENABLED")
    gmail_use_mock: bool = Field(default=True, alias="GMAIL_USE_MOCK")
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")

    # Gmail credentials (stubbed usage for now)
    gmail_client_id: str | None = Field(default=None, alias="GMAIL_CLIENT_ID")
    gmail_client_secret: str | None = Field(default=None, alias="GMAIL_CLIENT_SECRET")
    gmail_refresh_token: str | None = Field(default=None, alias="GMAIL_REFRESH_TOKEN")
    gmail_user_email: str | None = Field(default=None, alias="GMAIL_USER_EMAIL")

    # LLM configuration
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance for FastAPI dependency injection."""

    return Settings()  # type: ignore[call-arg]
