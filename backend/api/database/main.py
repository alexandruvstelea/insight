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


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB_NAME}"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


async def init_db():
    async with engine.begin() as conn:
        from .models.faculty import Faculty
        from .models.building import Building
        from .models.faculties_buildings import faculties_buildings
        from .models.room import Room
        from .models.programme import Programme
        from .models.professor import Professor
        from .models.faculties_professors import faculties_professors

        await conn.run_sync(AlchemyAsyncBase.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with session_factory() as session:
        try:
            yield session
        except IntegrityError as e:
            await session.rollback()
            raise e


class AlchemyAsyncBase(AsyncAttrs, DeclarativeBase):
    pass
