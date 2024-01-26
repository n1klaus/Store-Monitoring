#!/usr/bin/env bash

## Start celery worker
celery -A config.celery worker --loglevel=info & disown;

## Start uvicorn server
python3 main.py;

exit 0;
