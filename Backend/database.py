from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, sessionmaker, declarative_base

load_dotenv("Backend/postgresql.env")

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")

Base = declarative_base()

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB_NAME}")


Session = sessionmaker(bind=engine)
session = Session()
