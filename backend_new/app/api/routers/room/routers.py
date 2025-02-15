from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.room import RoomIn, RoomOut, RoomFilter
from app.services.implementations.room_service import RoomService
from app.core.database import get_session
from typing import Optional, Literal
from app.core.logging import logger

room_router = APIRouter(prefix="/room", tags=["room"])


@room_router.post("/", response_model=Optional[RoomOut])
async def create(room_data: RoomIn, db_session: AsyncSession = Depends(get_session)):
    return await RoomService(db_session).create(room_data)


@room_router.get("/", response_model=Optional[list[RoomOut]])
async def get_all(
    name: Optional[str] = None,
    unique_code: Optional[str] = None,
    session_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = RoomFilter(
        name=name,
        unique_code=unique_code,
        session_id=session_id,
    )

    return await RoomService(db_session).get_all(filters)


@room_router.get("/{room_id}", response_model=Optional[RoomOut])
async def get_by_id(room_id: int, db_session: AsyncSession = Depends(get_session)):
    return await RoomService(db_session).get_by_id(room_id)


@room_router.put("/{room_id}", response_model=Optional[RoomOut])
async def update(
    room_id: int,
    room_data: RoomIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await RoomService(db_session).update(room_id, room_data)


@room_router.delete("/{room_id}", response_model=str)
async def delete(room_id: int, db_session: AsyncSession = Depends(get_session)):
    return await RoomService(db_session).delete(room_id)


@room_router.get("/count/entities", response_model=Optional[int])
async def count(
    name: Optional[str] = None,
    unique_code: Optional[str] = None,
    session_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = RoomFilter(
        name=name,
        unique_code=unique_code,
        session_id=session_id,
    )

    return await RoomService(db_session).count(filters)
