from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
HOST = getenv("POSTGRES_HOST")
DB_NAME = getenv("POSTGRES_DB_NAME")

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}",
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session
