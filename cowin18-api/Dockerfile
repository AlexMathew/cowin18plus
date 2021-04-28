FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y && apt-get install gcc git -y
RUN pip install pipenv

RUN mkdir /code
ADD . /code/
WORKDIR /code

RUN pipenv install --system --dev