from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

EnvType = Literal["PROD", "DEV", "TEST"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    API_PREFIX: str = '/api'
    INSTANCE_ID: int = 1
    ENVIRONMENT: EnvType = "PROD"

    CORS_ORIGINS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]

    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    OPENAI_API_KEY: str | None


envs = Settings()
