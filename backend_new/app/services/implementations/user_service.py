from app.services.interfaces.i_user_service import IUserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserIn, UserOut
from typing import Optional
from app.schemas.user import UserFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class UserService(IUserService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
