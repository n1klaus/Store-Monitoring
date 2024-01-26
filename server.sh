#!/usr/bin/env bash

## Start celery worker
echo -e "\nStarting celery ..." && \
celery -A config.celery worker --loglevel=info & disown && \

# Wait for celery worker to start
sleep 5s && \

## Start uvicorn server
echo -e "\nStarting uvicorn server ..." && \
python3 main.py && \

exit 0;
