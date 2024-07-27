from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import RoomIn, RoomOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import RoomOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
rooms_router = APIRouter(prefix="/api/rooms")


@rooms_router.get("/", response_model=List[RoomOut], status_code=HTTPStatus.OK)
async def get_rooms(
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[RoomOut]:
    logger.info(f"Received GET request on endpoint /api/rooms from IP {client_ip}.")
    rooms = await RoomOperations(session).get_rooms(faculty_id)
    return rooms


@rooms_router.get("/{id}", response_model=RoomOut, status_code=HTTPStatus.OK)
async def get_room_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(f"Received GET request on endpoint /api/rooms/ip from IP {client_ip}.")
    room = await RoomOperations(session).get_room_by_id(id)
    return room


@rooms_router.post("/", response_model=RoomOut, status_code=HTTPStatus.CREATED)
async def add_room(
    room_data: RoomIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(f"Received POST request on endpoint /api/rooms from IP {client_ip}.")
    response = await RoomOperations(session).add_room(room_data)
    return response


@rooms_router.put("/{id}", response_model=RoomOut, status_code=HTTPStatus.OK)
async def update_room(
    id: int,
    new_room_data: RoomIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(f"Received PUT request on endpoint /api/rooms/id from IP {client_ip}.")
    response = await RoomOperations(session).update_room(id, new_room_data)
    return response


@rooms_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_room(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/rooms/id from IP {client_ip}."
    )
    response = await RoomOperations(session).delete_room(id)
    return response
