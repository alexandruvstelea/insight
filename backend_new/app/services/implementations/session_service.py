from app.services.interfaces.i_session_service import ISessionService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import Session
from app.schemas.session import SessionIn, SessionOut
from typing import Optional
from app.schemas.session import SessionFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class SessionService(ISessionService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
