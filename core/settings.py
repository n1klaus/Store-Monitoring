#!/usr/bin/python3

"""Settings Module"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Class to store app settings"""

    DEV_MODE: bool = True
    TEST_MODE: bool = True
    DEBUG_MODE: bool = True
    DEFAULT_TZ: str = 'America/Chicago'
    APP_HOST: str = '0.0.0.0'
    APP_PORT: str = 8000
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str | None = None
    CELERY_BROKER_URL: str = 'redis://localhost:6379/0'

    model_config = SettingsConfigDict(env_file='.env')

@lru_cache()
def get_settings():
    """Returns settings configuration"""
    settings = Settings()
    DATABASE_URL = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.\
                    format(settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME)
    setattr(settings, 'DATABASE_URL', DATABASE_URL)
    print(settings.DATABASE_URL)
    return settings
