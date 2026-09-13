"""
Centralized application settings.

Values are read from environment variables (see ../../.env.example at the
project root). Nothing here should ever contain a hardcoded secret or API
key -- they are injected at runtime via the environment / .env file.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "PharmaQMS Complaint Management API"
    ENVIRONMENT: str = "development"

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # PostgreSQL (not wired up yet in Phase 1 -- present so the next phase
    # only needs to add a db/session.py implementation, not new config).
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/pharma_complaints"

    # AI layer (used in a later phase). Never hardcode this value -- it must
    # come from the environment.
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "gemma2-9b-it"


@lru_cache
def get_settings() -> Settings:
    return Settings()
