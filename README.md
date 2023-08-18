## Installation
``` Python
# Install Python 3.11 (if not present)
sudo apt update
sudo apt install python3.11-full
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 100

# Set Python 3.11 as default
sudo update-alternatives --config python3

# install postgresql
sudo apt-get -y install postgresql postgresql-contrib

# Create python virtual environment with python 3.11
python3 -m virtualenv .venv -p /usr/bin/python3.11

# activate virtual environment
. .venv/bin/activate

# Upgrade pip for python 3.11
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# install necessary python packages
pip install -r requirements.txt
```

## Starting the app
``` Python
# Start the redis server
sudo service redis-server start

# Start the postgresql server
sudo service postgresql start

# Connecting to the redis cli
redis-cli -h <host> -p <port> --user <user> --pass <pass>
# redis-cli -u <server-uri>

# Connecting to the postgresql cli
psql -h <host> -p <port> -U <user> -P <pass>

# Start running the app
python main.py
```

## TESTING
