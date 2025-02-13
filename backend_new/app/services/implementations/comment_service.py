from app.services.interfaces.i_comment_service import ICommentService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.schemas.comment import CommentIn, CommentOut
from typing import Optional
from app.schemas.comment import CommentFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class CommentService(ICommentService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
