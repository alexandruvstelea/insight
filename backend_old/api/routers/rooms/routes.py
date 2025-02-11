from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import RoomIn, RoomOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import RoomOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)
rooms_router = APIRouter(prefix="/api/rooms")


@authorize(role=["admin"])
@rooms_router.get(
    "/",
    response_model=List[RoomOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_rooms(
    faculty_id: int = None,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[RoomOut]:
    logger.info(f"Received GET request on endpoint /api/rooms from IP {client_ip}.")
    rooms = await RoomOperations(session).get_rooms(faculty_id)
    return rooms


@authorize(role=["admin"])
@rooms_router.get(
    "/{id}",
    response_model=RoomOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_room_by_id(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(
        f"Received GET request on endpoint /api/rooms/{id} from IP {client_ip}."
    )
    room = await RoomOperations(session).get_room_by_id(id)
    return room


@authorize(role=["admin"])
@rooms_router.post(
    "/",
    response_model=RoomOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_room(
    room_data: RoomIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(f"Received POST request on endpoint /api/rooms from IP {client_ip}.")
    response = await RoomOperations(session).add_room(room_data)
    return response


@authorize(role=["admin"])
@rooms_router.put(
    "/{id}",
    response_model=RoomOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def update_room(
    id: int,
    new_room_data: RoomIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RoomOut:
    logger.info(
        f"Received PUT request on endpoint /api/rooms/{id} from IP {client_ip}."
    )
    response = await RoomOperations(session).update_room(id, new_room_data)
    return response


@authorize(role=["admin"])
@rooms_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_room(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/rooms/{id} from IP {client_ip}."
    )
    response = await RoomOperations(session).delete_room(id)
    return response


@rooms_router.get(
    "/count/entities",
    response_model=int,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_rooms_count(
    faculty_id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> int:
    logger.info(
        f"Received GET request on endpoint /api/rooms/count/entities from IP {client_ip}."
    )
    count = await RoomOperations(session).get_entities_count(faculty_id)
    return count
