# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV FLASK_APP=silently-failing

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . .

EXPOSE 8050

ENTRYPOINT ["gunicorn", "silently-failing:app", "-w 2", "-b 0.0.0.0:8050", "--reload"]