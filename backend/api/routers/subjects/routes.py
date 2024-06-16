from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import RoomIn, RoomOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import RoomOperations
from http import HTTPStatus
from typing import List

rooms_router = APIRouter(prefix="/api/rooms")


@rooms_router.get("/", response_model=List[RoomOut], status_code=HTTPStatus.OK)
async def get_rooms(
    session: AsyncSession = Depends(get_session),
) -> List[RoomOut]:
    response = await RoomOperations(session).get_rooms()
    return response


@rooms_router.get("/{id}", response_model=RoomOut, status_code=HTTPStatus.OK)
async def get_room_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> RoomOut:
    response = await RoomOperations(session).get_room_by_id(id)
    return response


@rooms_router.post("/", response_model=RoomOut, status_code=HTTPStatus.CREATED)
async def add_room(
    room_data: RoomIn, session: AsyncSession = Depends(get_session)
) -> RoomOut:
    response = await RoomOperations(session).add_room(room_data)
    return response


@rooms_router.put("/{id}", response_model=RoomOut, status_code=HTTPStatus.OK)
async def update_room(
    id: int, new_room_data: RoomIn, session: AsyncSession = Depends(get_session)
) -> RoomOut:
    response = await RoomOperations(session).update_room(id, new_room_data)
    return response


@rooms_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_room(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await RoomOperations(session).delete_room(id)
    return response
