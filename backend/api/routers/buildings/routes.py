from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import BuildingIn, BuildingOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import BuildingsOperations
from http import HTTPStatus
from typing import List
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
import logging


buildings_router = APIRouter(prefix="/api/buildings")
logger = logging.getLogger(__name__)


# @authorize(role=["admin"])
@buildings_router.get(
    "/",
    response_model=List[BuildingOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_buildings(
    faculty_id: int = None,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[BuildingOut]:
    logger.info(f"Received GET request on endpoint /api/buildings from IP {client_ip}.")
    buildings = await BuildingsOperations(session).get_buildings(faculty_id)
    return buildings


# @authorize(role=["admin"])
@buildings_router.get(
    "/{id}",
    response_model=BuildingOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_building_by_id(
    id: int,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> BuildingOut:
    logger.info(
        f"Received GET request on endpoint /api/buildings/id from IP {client_ip}."
    )
    building = await BuildingsOperations(session).get_building_by_id(id)
    return building


# @authorize(role=["admin"])
@buildings_router.post(
    "/",
    response_model=BuildingOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_building(
    building_data: BuildingIn,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> BuildingOut:
    logger.info(
        f"Received POST request on endpoint /api/buildings from IP {client_ip}."
    )
    response = await BuildingsOperations(session).add_building(building_data)
    return response


# @authorize(role=["admin"])
@buildings_router.put(
    "/{id}",
    response_model=BuildingOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def update_building(
    id: int,
    new_building_data: BuildingIn,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> BuildingOut:
    logger.info(
        f"Received PUT request on endpoint /api/buildings/id from IP {client_ip}."
    )
    response = await BuildingsOperations(session).update_building(id, new_building_data)
    return response


# @authorize(role=["admin"])
@buildings_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_building(
    id: int,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/buildings/id from IP {client_ip}."
    )
    response = await BuildingsOperations(session).delete_building(id)
    return response
