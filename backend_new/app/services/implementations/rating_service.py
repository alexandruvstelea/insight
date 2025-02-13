from app.services.interfaces.i_rating_service import IRatingService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rating import Rating
from app.schemas.rating import RatingIn, RatingOut
from typing import Optional
from app.schemas.rating import RatingFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class RatingService(IRatingService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
