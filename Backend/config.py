from dotenv import load_dotenv
import os

load_dotenv("postgresql.env")

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")


class Config:
    SECRET_KEY = "PSjf6fjKbz9LqDuj"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
