from ...database.models.weeks import Week
from .schemas import WeekOut
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


def week_to_out(week: Week):
    return WeekOut(id=week.id, start=week.start, end=week.end, semester=week.semester)


async def get_week_from_timestamp(session: AsyncSession, timestamp: datetime) -> Week:
    result = await session.execute(
        select(Week).where(Week.start <= timestamp, Week.end >= timestamp)
    )
    week = result.scalars().first()
    if week:
        return week
    raise HTTPException(
        status_code=404,
        detail=f"Could not find current week for timestamp={timestamp}.",
    )
