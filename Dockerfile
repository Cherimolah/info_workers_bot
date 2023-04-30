# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY http_api http_api
COPY telegram_bot telegram_bot

CMD ["python3", "http_api/main.py"]
CMD ["python3", "telegram_bot/main.py"]