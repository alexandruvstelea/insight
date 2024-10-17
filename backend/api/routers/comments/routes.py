from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import CommentIn, CommentOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import CommentOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
comments_routes = APIRouter(prefix="/api/comments")


@comments_routes.get(
    "/",
    response_model=List[CommentOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_comments(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[CommentOut]:
    logger.info(f"Received GET request on endpoint /api/comments from IP {client_ip}.")
    comments = await CommentOperations(session).get_comments(
        professor_id, subject_id, session_type, limit, offset
    )
    return comments


@comments_routes.post(
    "/",
    response_model=CommentOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_comment(
    comment_data: CommentIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> CommentOut:
    logger.info(f"Received POST request on endpoint /api/comments from IP {client_ip}.")
    response = await CommentOperations(session).add_comment(comment_data)
    return response


@authorize(role=["admin"])
@comments_routes.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_comment(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/comments/id from IP {client_ip}."
    )
    response = await CommentOperations(session).delete_comment(id)
    return response
