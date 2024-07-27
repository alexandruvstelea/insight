from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import WeekIn, WeekOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import WeekOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
weeks_routes = APIRouter(prefix="/api/weeks")


@weeks_routes.get("/", response_model=List[WeekOut], status_code=HTTPStatus.OK)
async def get_weeks(
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[WeekOut]:
    logger.info(f"Received GET request on endpoint /api/weeks from IP {client_ip}.")
    weeks = await WeekOperations(session).get_weeks()
    return weeks


@weeks_routes.post("/", response_model=List[WeekOut], status_code=HTTPStatus.CREATED)
async def add_weeks(
    week_data: WeekIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[WeekOut]:
    logger.info(f"Received POST request on endpoint /api/weeks from IP {client_ip}.")
    response = await WeekOperations(session).add_weeks(week_data)
    return response


@weeks_routes.delete("/", status_code=HTTPStatus.OK)
async def delete_weeks(
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(f"Received DELETE request on endpoint /api/weeks from IP {client_ip}.")
    response = await WeekOperations(session).delete_weeks()
    return response
