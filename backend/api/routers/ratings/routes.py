from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import RatingIn, RatingOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import RatingOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
ratings_routes = APIRouter(prefix="/api/ratings")


@ratings_routes.get("/", response_model=List[RatingOut], status_code=HTTPStatus.OK)
async def get_ratings(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[RatingOut]:
    logger.info(f"Received GET request on endpoint /api/ratings from IP {client_ip}.")
    response = await RatingOperations(session).get_ratings(
        professor_id, subject_id, session_type
    )
    return response


@ratings_routes.post("/", response_model=RatingOut, status_code=HTTPStatus.CREATED)
async def add_rating(
    rating_data: RatingIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RatingOut:
    logger.info(f"Received POST request on endpoint /api/ratings from IP {client_ip}.")
    response = await RatingOperations(session).add_rating(rating_data)
    return response
