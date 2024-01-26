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
## Start celery worker
celery -A config.celery worker --loglevel=info

# FASTAPI
## Start uvicorn server
python3 main.py
```

## TESTING
```
# Postman Collection
https://www.postman.com/n1klaus/workspace/store-monitoring/overview

# Pytest

```
