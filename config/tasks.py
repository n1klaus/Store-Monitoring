#!/usr/bin/env python3
"""Celery task handler module"""
from functools import lru_cache

from celery import Celery

from config.settings import get_settings

settings = get_settings()


@lru_cache()
def get_celery():
    """Returns celery instance"""
    celery: Celery = Celery("store_monitoring", include=["jobs.job_engine"])
    try:
        celery.config_from_object(settings, force=True, namespace="CELERY")
        return celery
    finally:
        celery.close()
