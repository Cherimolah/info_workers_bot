import os
from dotenv import load_dotenv

load_dotenv(".env")

USER = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE_NAME")
