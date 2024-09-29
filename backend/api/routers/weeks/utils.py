from ...database.models.weeks import Week
from .schemas import WeekOut
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def week_to_out(week: Week):
    if week:
        logger.info(f"Converting week {week.id} to WeekOut format.")
        return WeekOut(
            id=week.id, start=week.start, end=week.end, semester=week.semester
        )
    return None


async def get_week_from_timestamp(session: AsyncSession, timestamp: datetime) -> Week:
    try:
        if timestamp:
            logger.info(f"Determining week from timestamp {timestamp}.")
            result = await session.execute(
                select(Week).where(Week.start <= timestamp, Week.end >= timestamp)
            )
            week = result.scalars().first()
            if week:
                return week
            raise HTTPException(
                status_code=404,
                detail=f"Could not find current week for timestamp {timestamp}.",
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while determining week from timestamp {timestamp}."
        )
        raise e
