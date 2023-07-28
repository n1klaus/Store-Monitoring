#!/usr/bin/python3

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Class to store app settings"""

    DEV_MODE: bool
    TEST_MODE: bool
    DEBUG_MODE: bool
    DEFAULT_TZ: str = 'America/Chicago'
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    CELERY_BROKER_URL: str = 'redis://localhost:6379/0'

    model_config = SettingsConfigDict(env_file='.env')

@lru_cache()
def get_settings():
    return Settings()