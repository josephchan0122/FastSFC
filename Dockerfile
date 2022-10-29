FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python nodejs npm -y --no-install-recommends
RUN apt-get install python-pip -y && npm install -g npm-run-all
RUN apt-get install libmysqld-dev libpq-dev libxml2-dev libxslt1-dev  -y --no-install-recommends

WORKDIR /app

COPY ./requirements.pip ./

RUN pip install -r requirements.pip
