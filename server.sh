#!/usr/bin/env bash

# Run celery with lower permissions
mkdir -p /var/run/celery /var/log/celery && \
chown -R nobody:nogroup /var/run/celery /var/log/celery && \
# rc-service rabbitmq-server start && \
# sleep 5s && \

## Start celery worker
echo -e "\nStarting celery ..." && \
celery -A config.celery worker \
    --loglevel=info --logfile=/var/log/celery/worker-prod.log \
    --statedb=/var/run/celery/worker-prod@%h.state \
    --uid=nobody --gid=nogroup \
    & disown && \

# Wait for celery worker to start
sleep 5s && \

## Start uvicorn server
echo -e "\nStarting uvicorn server ..." && \
python3 main.py && \

exit 0;
