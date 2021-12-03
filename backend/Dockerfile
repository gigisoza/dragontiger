FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get -y install netcat gcc curl

COPY req.txt .
RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY . .


FROM python:3.9.6-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .
