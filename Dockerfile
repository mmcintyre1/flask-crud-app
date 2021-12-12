# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV FLASK_APP=silently-failing

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["gunicorn", "silently-failing:app", "-w 2", "-b 0.0.0.0:8050"]