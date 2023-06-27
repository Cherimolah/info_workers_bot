import os
from dotenv import load_dotenv, find_dotenv

load_dotenv("/home/ilya/PycharmProjects/info_workers_bot/.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
