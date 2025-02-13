from app.services.interfaces.i_professor_service import IProfessorService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.professor import Professor
from app.schemas.professor import ProfessorIn, ProfessorOut
from typing import Optional
from app.schemas.professor import ProfessorFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ProfessorService(IProfessorService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
