from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import CommentIn, CommentOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import CommentOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
comments_routes = APIRouter(prefix="/api/comments")


@comments_routes.get("/", response_model=List[CommentOut], status_code=HTTPStatus.OK)
async def get_comments(
    professor_id: int = None,
    subject_id: int = None,
    session_type: str = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[CommentOut]:
    logger.info(f"Received GET request on endpoint /api/comments from IP {client_ip}.")
    comments = await CommentOperations(session).get_comments(
        professor_id, subject_id, session_type
    )
    return comments


@comments_routes.post("/", response_model=CommentOut, status_code=HTTPStatus.CREATED)
async def add_comment(
    comment_data: CommentIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> CommentOut:
    logger.info(f"Received POST request on endpoint /api/comments from IP {client_ip}.")
    response = await CommentOperations(session).add_comment(comment_data)
    return response


@comments_routes.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_comment(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/comments/id from IP {client_ip}."
    )
    response = await CommentOperations(session).delete_comment(id)
    return response
