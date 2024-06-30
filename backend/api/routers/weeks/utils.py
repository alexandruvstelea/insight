from ...database.models.weeks import Week
from .schemas import WeekOut
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def week_to_out(week: Week):
    return WeekOut(id=week.id, start=week.start, end=week.end, semester=week.semester)
