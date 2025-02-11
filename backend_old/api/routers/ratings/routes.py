from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import RatingIn, RatingOut, RatingAverageOut, WeekRatings
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import RatingOperations
from fastapi_limiter.depends import RateLimiter
from http import HTTPStatus
from typing import List
import logging
from ...utility.vote_limiter import vote_limiter

logger = logging.getLogger(__name__)
ratings_routes = APIRouter(prefix="/api/ratings")


@ratings_routes.get(
    "/",
    response_model=List[RatingOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_ratings(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[RatingOut]:
    logger.info(f"Received GET request on endpoint /api/ratings from IP {client_ip}.")
    ratings = await RatingOperations(session).get_ratings(
        professor_id, subject_id, session_type
    )
    return ratings


@ratings_routes.get(
    "/average",
    response_model=RatingAverageOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_average_ratings(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RatingAverageOut:
    logger.info(
        f"Received GET request on endpoint /api/ratings/average from IP {client_ip}."
    )
    ratings = await RatingOperations(session).get_ratings_average(
        professor_id, subject_id, session_type
    )
    return ratings


@ratings_routes.get(
    "/average/programmes",
    response_model=dict[str, float],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_average_ratings(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> dict[str, float]:
    logger.info(
        f"Received GET request on endpoint /api/ratings/average/programmes from IP {client_ip}."
    )
    ratings = await RatingOperations(session).get_ratings_average_per_programme(
        professor_id, subject_id, session_type
    )
    return ratings


@ratings_routes.get(
    "/history",
    response_model=dict[str, WeekRatings],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_graph_ratings(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> dict[str, WeekRatings]:
    logger.info(
        f"Received GET request on endpoint /api/ratings/history from IP {client_ip}."
    )
    ratings = await RatingOperations(session).get_ratings_graph(
        professor_id, subject_id, session_type
    )
    return ratings


@ratings_routes.post(
    "/",
    response_model=RatingOut,
    status_code=HTTPStatus.CREATED,
)
async def add_rating(
    rating_data: RatingIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> RatingOut:
    logger.info(f"Received POST request on endpoint /api/ratings from IP {client_ip}.")
    if client_ip:
        await vote_limiter(client_ip, session)
    response = await RatingOperations(session).add_rating(rating_data)
    return response


@ratings_routes.get(
    "/count/entities",
    response_model=int,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_ratings_count(
    faculty_id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> int:
    logger.info(
        f"Received GET request on endpoint /api/ratings/count/entities from IP {client_ip}."
    )
    count = await RatingOperations(session).get_entities_count(faculty_id)
    return count
