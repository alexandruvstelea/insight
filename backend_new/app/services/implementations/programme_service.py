from app.services.interfaces.i_programme_service import IProgrammeService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.programme import Programme
from app.schemas.programme import ProgrammeIn, ProgrammeOut
from typing import Optional
from app.schemas.programme import ProgrammeFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ProgrammeService(IProgrammeService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
