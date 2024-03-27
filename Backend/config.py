from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
HOST = getenv("POSTGRES_HOST")
DB_NAME = getenv("POSTGRES_DB_NAME")


class Config:
    SECRET_KEY = getenv("FLASK_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
