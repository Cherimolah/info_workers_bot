# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY http_api http_api
COPY telegram_bot telegram_bot

EXPOSE 8001

FROM postgres:14.8
EXPOSE 5432

CMD ["python3", "async_http_api/main.py"]