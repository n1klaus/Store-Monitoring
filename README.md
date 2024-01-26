## Installation
``` Python
# Install Python 3.10 (if not system default)
sudo apt update
sudo apt install python3.10-full
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 100

# Set Python 3.10 as default
sudo update-alternatives --config python3

# install postgresql
sudo apt-get -y install postgresql postgresql-contrib

# install redis
sudo apt-get -y install redis

# install celery
sudo apt install -y celery

# Create python virtual environment with python 3.10
python3 -m virtualenv .venv -p /usr/bin/python3.10

# activate virtual environment
. .venv/bin/activate

# Upgrade pip for python 3.10
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# install necessary python packages
pip install -r requirements.txt
```

## Starting the services
``` Python
# REDIS
## Start the redis server
sudo service redis-server restart

## Create redis user and password
cat setup_dev_redis.txt | redis-cli --pipe

## Connecting to the redis cli
redis-cli -h 127.0.0.1 -p 6379 --user redis_dev --pass redis_dev_pwd -n 0
## or
redis-cli -u "redis://redis_dev:redis_dev_pwd@127.0.0.1:6379/0"

# POSTGRESQL
## Configure postgres to trust local connections and disable password authentication
sudo vim /etc/postgresql/14/main/pg_hba.conf

### change the following lines
host    all             all             127.0.0.1/32            trust
host    replication     all             127.0.0.1/32            trust

## Restart postgresql server
sudo service postgresql restart

## Create the database and user from postgres cli
cat setup_dev_postgres.sql | psql -h 127.0.0.1 -p 5432 -U postgres

## Connecting to postgresql using cli
psql -h 127.0.0.1 -p 5432 -d store_dev_db -U store_dev -W
## or
psql "postgres://store_dev:store_dev_pwd@localhost:5432/store_dev_db"

# CELERY
## Check running celery worker nodes
ps aux|grep 'celery worker'

## Close any existing celery worker nodes
pkill -f "celery worker"

## Start celery worker
celery -A config.celery worker --loglevel=info

# FASTAPI
## Start uvicorn server
python3 main.py
```

## Docker
```Bash
# Creating a volume
docker volume create postgres_data
docker volume create postgres_config
docker volume create redis_data
docker volume create redis_logs

# Creating a network
docker network create mynet

# Running a local postgresql container
docker run --rm --detach \
    --name store-monitoring-db \
	--volume postgres_data:/var/lib/postgresql \
	--volume postgresql_config:/etc/postgresql \
	--network mynet \
	--publish 5432:5432 \
	-e POSTGRES_PASSWORD=store_dev_pwd \
	-e POSTGRES_USER=store_dev \
	-e POSTGRES_DB=store_dev_db \
	postgres:15-alpine

# Running a local redis container
docker run --rm --detach \
    --name store-monitoring-redis \
    --network mynet \
    --volume redis_data:/var/run/celery \
    --volume redis_logs:/var/log/celery \
    redis:7-alpine

# Running a local rabbitmq container
docker run --rm --detach \
    --name store-monitoring-rabbitmq \
    --network mynet \
    rabbitmq:3-management-alpine

# Build docker image for the application
docker build -t store_monitoring .

# Run docker container for the application
docker run --rm --detach\
    --name store-monitoring \
    --network mynet \
    --publish 8000:8000 \
    store_monitoring

docker exec -it store-monitoring bash

# Push docker image to Github Container Registry
docker tag store_monitoring ghcr.io/n1klaus/store_monitoring:0.1.1
docker tag store_monitoring ghcr.io/n1klaus/store_monitoring:latest
docker push ghcr.io/n1klaus/store_monitoring:latest
```

## TESTING
```
# Postman Collection
https://www.postman.com/n1klaus/workspace/store-monitoring/overview

# Pytest

```
