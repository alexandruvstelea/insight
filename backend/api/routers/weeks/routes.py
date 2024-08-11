from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import WeekIn, WeekOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import WeekOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from typing import List
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
import logging

logger = logging.getLogger(__name__)
weeks_routes = APIRouter(prefix="/api/weeks")


# @authorize(role=["admin"])
@weeks_routes.get(
    "/",
    response_model=List[WeekOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_weeks(
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[WeekOut]:
    logger.info(f"Received GET request on endpoint /api/weeks from IP {client_ip}.")
    weeks = await WeekOperations(session).get_weeks()
    return weeks


# @authorize(role=["admin"])
@weeks_routes.post(
    "/",
    response_model=List[WeekOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_weeks(
    week_data: WeekIn,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[WeekOut]:
    logger.info(f"Received POST request on endpoint /api/weeks from IP {client_ip}.")
    response = await WeekOperations(session).add_weeks(week_data)
    return response


# @authorize(role=["admin"])
@weeks_routes.delete(
    "/",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_weeks(
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(f"Received DELETE request on endpoint /api/weeks from IP {client_ip}.")
    response = await WeekOperations(session).delete_weeks()
    return response
