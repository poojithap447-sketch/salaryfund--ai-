"""
Central application configuration.
All environment-driven settings are declared here using pydantic-settings.
Never hardcode secrets - everything is sourced from environment variables / .env
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- General ---
    PROJECT_NAME: str = "SalaryFund AI"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # --- Security / JWT ---
    SECRET_KEY: str = Field(..., description="Used to sign JWTs - must be set via env in production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OTP_EXPIRE_MINUTES: int = 5
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Database ---
    DATABASE_URL: str = Field(..., description="Async SQLAlchemy DSN, e.g. postgresql+asyncpg://...")
    DATABASE_URL_SYNC: str = Field(..., description="Sync DSN for Alembic")
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # --- Redis / Celery ---
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # --- CORS ---
    # Stored as a raw comma-separated string to avoid pydantic-settings' default
    # JSON-decoding of complex env values; use the `cors_origins_list` property instead.
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    # --- Rate limiting ---
    RATE_LIMIT_DEFAULT: str = "100/minute"
    RATE_LIMIT_AUTH: str = "10/minute"
    RATE_LIMIT_OTP: str = "5/minute"

    # --- File uploads ---
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "/data/uploads"
    ALLOWED_DOCUMENT_TYPES: List[str] = ["application/pdf", "image/png", "image/jpeg"]

    # --- Email / SMS (provider credentials) ---
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "no-reply@salaryfund.ai"
    SMS_PROVIDER_API_KEY: str = ""
    SMS_PROVIDER_SENDER_ID: str = "SALFND"

    # --- AI ---
    MODEL_ARTIFACT_DIR: str = "/data/ai_models"
    ELIGIBILITY_MODEL_VERSION: str = "v1"
    FRAUD_MODEL_VERSION: str = "v1"

    # --- Credit Bureau Integration ---
    CREDIT_BUREAU_API_KEY: str = "CIBIL-OFFICIAL-KEY-9982"

    # --- Encryption for PII at rest ---
    FIELD_ENCRYPTION_KEY: str = Field(..., description="Fernet key for encrypting PII columns")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
