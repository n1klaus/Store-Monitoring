#!/usr/bin/python3
"""Settings Module"""
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Class to store app settings"""

    DEV_MODE: bool = True
    TEST_MODE: bool = True
    DEBUG_MODE: bool = True
    DEFAULT_TZ: str = "America/Chicago"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str | None = None
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_INSTANCE: str
    CELERY_BROKER_URL: str = "amqp://guest:guest@127.0.0.1:5672"
    result_backend: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings():
    """Returns configuration settings"""
    settings: Settings = Settings()

    DATABASE_URL = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        settings.DB_USERNAME,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        settings.DB_PORT,
        settings.DB_NAME,
    )
    setattr(settings, "DATABASE_URL", DATABASE_URL)

    result_backend = "db+" + settings.DATABASE_URL
    setattr(settings, "result_backend", result_backend)

    return settings
