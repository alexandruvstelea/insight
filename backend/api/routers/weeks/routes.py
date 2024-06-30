from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import WeekIn, WeekOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import WeekOperations
from http import HTTPStatus
from typing import List

weeks_routes = APIRouter(prefix="/api/weeks")


@weeks_routes.get("/", response_model=List[WeekOut], status_code=HTTPStatus.OK)
async def get_weeks(
    session: AsyncSession = Depends(get_session),
) -> List[WeekOut]:
    response = await WeekOperations(session).get_weeks()
    return response


@weeks_routes.post("/", response_model=List[WeekOut], status_code=HTTPStatus.CREATED)
async def add_weeks(
    week_data: WeekIn, session: AsyncSession = Depends(get_session)
) -> List[WeekOut]:
    response = await WeekOperations(session).add_weeks(week_data)
    return response


@weeks_routes.delete("/", status_code=HTTPStatus.OK)
async def delete_weeks(session: AsyncSession = Depends(get_session)) -> str:
    response = await WeekOperations(session).delete_weeks()
    return response
