#!/usr/bin/env bash

## Close any existing celery worker nodes
pkill -f "celery worker" && \

## Start celery worker
celery -A config.celery worker --loglevel=info & disown && \

# Wait for celery worker to start
sleep 5s && \

## Start uvicorn server
python3 main.py && \

exit 0;
