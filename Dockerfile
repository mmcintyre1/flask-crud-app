# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV FLASK_APP=${FLASK_APP}

# prevents python from generating a .pyc file
ENV PYTHONDONTWRITEBYTECODE 1
# prevents python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . .

# gunicorn
EXPOSE 5000

ENTRYPOINT ["sh", "./entrypoint.sh"]