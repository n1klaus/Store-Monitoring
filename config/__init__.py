#!/usr/bin/python3
"""Config Module"""
from config.settings import get_settings
from config.tasks import get_celery

settings = get_settings()

celery = get_celery()
