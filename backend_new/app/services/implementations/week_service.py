from app.services.interfaces.i_week_service import IWeekService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.week import Week
from app.schemas.week import WeekIn, WeekOut
from typing import Optional
from app.schemas.week import WeekFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class WeekService(IWeekService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
