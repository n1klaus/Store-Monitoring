# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# Add the testing repository to your Alpine Linux Docker
# RUN echo @testing http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
# # install RabbitMQ from testing branch
# RUN apk add rabbitmq-server@testing

# # configure Erlang cookie
# RUN touch /usr/lib/rabbitmq/.erlang.cookie \
#  && echo your-favourite-erlang-cookie > /usr/lib/rabbitmq/.erlang.cookie \
#  && chown rabbitmq:rabbitmq /usr/lib/rabbitmq/.erlang.cookie \
#  && chmod 700 /usr/lib/rabbitmq/.erlang.cookie

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev openrc bash vim curl \
    && pip install psycopg2

# install python packages
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .

RUN chmod +x ./server.sh

EXPOSE 8000

CMD ["./server.sh"]
