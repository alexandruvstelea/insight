from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)
from ..config import settings
import logging

logger = logging.getLogger(__name__)


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB_NAME}"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


async def init_db():
    logger.info("Initializing database.")
    async with engine.begin() as conn:
        from .models.faculty import Faculty
        from .models.building import Building
        from .models.faculties_buildings import faculties_buildings
        from .models.room import Room
        from .models.programme import Programme
        from .models.professor import Professor
        from .models.faculties_professors import faculties_professors
        from .models.subject import Subject
        from .models.programmes_subjects import programmes_subjects
        from .models.session import Session
        from .models.weeks import Week
        from .models.ratings import Rating
        from .models.comments import Comment
        from .models.user import User

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
