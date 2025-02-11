from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)
from typing import AsyncGenerator
from app.core.config import settings
from app.core.logging import logger

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    logger.info("Initializing database.")
    async with engine.begin() as conn:
        from app.models.faculty import Faculty
        from app.models.building import Building
        from app.models.faculty_building import faculties_buildings
        from app.models.room import Room
        from app.models.programme import Programme
        from app.models.professor import Professor
        from app.models.faculty_professor import faculties_professors
        from app.models.subject import Subject
        from app.models.programme_subject import programmes_subjects
        from app.models.session import Session
        from app.models.week import Week
        from app.models.rating import Rating
        from app.models.comment import Comment
        from app.models.user import User
        from app.models.vote_limiter import VoteLimiter

        await conn.run_sync(AlchemyAsyncBase.metadata.create_all)
        logger.info("Database initialization complete.")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    logger.info("Retrieving database session.")
    session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with session_factory() as session:
        try:
            yield session
        except IntegrityError as e:
            logger.error(
                "An integrity error has occured while retrieving database session."
            )
            await session.rollback()
            raise e


class AlchemyAsyncBase(AsyncAttrs, DeclarativeBase):
    pass
