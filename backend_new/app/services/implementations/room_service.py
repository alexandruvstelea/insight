from app.services.interfaces.i_room_service import IRoomService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room
from app.schemas.room import RoomIn, RoomOut
from typing import Optional
from app.schemas.room import RoomFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class RoomService(IRoomService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
