from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CommentOut, CommentIn
from ...database.models.comments import Comment
from sqlalchemy import select, and_, func
from typing import List
from fastapi import HTTPException
from .utils import comment_to_out
import logging
from ...database.models.session import Session
from ..sessions.utils import get_session_from_timestamp
from ..subjects.utils import get_session_professor
from ...utility.error_parsing import format_integrity_error
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class CommentOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_comments(
        self, professor_id: int, subject_id: int, session_type: str
    ) -> List[CommentOut]:
        try:
            filters = []
            if professor_id:
                filters.append(Comment.professor_id == professor_id)
            if subject_id:
                filters.append(Comment.subject_id == subject_id)
            if session_type:
                filters.append(Comment.session_type == session_type)
            if filters:
                logger.info(f"Retrieving comments from database with provided filters.")
                query = select(Comment).where(and_(*filters))
            else:
                logger.info(f"Retrieving all comments from database.")
                query = select(Comment)
            result = await self.session.execute(query)
            comments = result.scalars().unique().all()
            if comments:
                logger.info("Succesfully retrieved all comments from database.")
                return [comment_to_out(comment) for comment in comments]
            logger.error("No comments found.")
            raise HTTPException(status_code=404, detail="No comments found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving comments:\n{e}"
            )
            raise e

    async def add_comment(self, comment_data: CommentIn) -> CommentOut:
        try:
            logger.info(f"Adding to database comment {comment_data}.")
            comment_session: Session = await get_session_from_timestamp(
                self.session, comment_data.timestamp, comment_data.room_id
            )
            if not comment_data.programme_id in [
                programme.id for programme in comment_session.subject.programmes
            ]:
                logger.error(
                    f"Programme ID {comment_data.programme_id} is not valid for current session."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Programme ID {comment_data.programme_id} is not valid for current session.",
                )
            if comment_data.room_id != comment_session.room_id:
                logger.error(
                    f"Room ID {comment_data.programme_id} is not valid for current session."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Room ID {comment_data.programme_id} is not valid for current session.",
                )
            new_comment = Comment(
                text=comment_data.text,
                subject_id=comment_session.subject_id,
                timestamp=comment_data.timestamp,
                programme_id=comment_data.programme_id,
                room_id=comment_data.room_id,
                professor_id=await get_session_professor(
                    self.session, comment_session.subject_id, comment_session.type
                ),
                faculty_id=comment_session.faculty_id,
            )
            self.session.add(new_comment)
            await self.session.commit()
            await self.session.refresh(new_comment)
            logger.info("Succesfully added new comment to database.")
            return comment_to_out(new_comment)
        except IntegrityError as e:
            error = format_integrity_error(e)
            logger.error(
                f"An integrity error has occured while adding comment to database:\n{e}"
            )
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding comment to databse:\n{e}"
            )
            raise e

    async def delete_comment(self, id: int) -> str:
        try:
            logger.info(f"Deleting comment with ID {id}.")
            comment = await self.session.get(Comment, id)
            if comment:
                await self.session.delete(comment)
                await self.session.commit()
                logger.info(f"Succesfully deleted comment with ID {id}.")
                return JSONResponse(f"Comment with ID {id} deleted.")
            logger.error(f"No comment with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No comment with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting comment with ID {id}:\n{e}"
            )
            raise e
