from app.services.interfaces.i_subject_service import ISubjectService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subject import Subject
from app.schemas.subject import SubjectIn, SubjectOut
from typing import Optional
from app.schemas.subject import SubjectFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class SubjectService(ISubjectService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
