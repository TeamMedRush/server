from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    APP_NAME: str = 'MedRush API'
    DEBUG: bool = False
    API_PREFIX: str = '/api'
    CORS_ORIGINS: list[str] = [
        'http://localhost:3001',
        'http://localhost:3002',
        'http://localhost:3003',
        'http://localhost:3004',
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
