from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CommentOut, CommentIn
from ...database.models.comments import Comment
from ...database.models.room import Room
from sqlalchemy import select, and_, desc, func
from typing import List, Optional
from fastapi import HTTPException
from .utils import comment_to_out
import logging
from ...database.models.session import Session
from ..sessions.utils import get_session_from_timestamp
from ..subjects.utils import get_session_professor
from ...utility.error_parsing import format_integrity_error
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from ..buildings.utils import check_location_distance
import pytz

logger = logging.getLogger(__name__)


class CommentOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_comments(
        self,
        professor_id: int,
        subject_id: int,
        session_type: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[CommentOut]:
        try:
            filters = []
            if professor_id:
                filters.append(Comment.professor_id == professor_id)
            if subject_id:
                filters.append(Comment.subject_id == subject_id)
            if session_type:
                filters.append(Comment.session_type == session_type)

            query = select(Comment)

            if filters:
                logger.info(f"Retrieving comments from database with provided filters.")
                query = query.where(and_(*filters))

            query = query.order_by(desc(Comment.timestamp))

            if limit:
                logger.info(f"Comments query limit is {limit}.")
                query = query.limit(limit)
            if offset:
                logger.info(f"Comments query offset is {offset}.")
                query = query.offset(offset)

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
            if len(comment_data.text) > 500:
                logger.error(
                    f"Comment text is too long (lenght {len(comment_data.text)}). Maximum text lenght is 500."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Comment text is too long (lenght {len(comment_data.text)}). Maximum text lenght is 500.",
                )
            if len(comment_data.text) < 10:
                logger.error(
                    f"Comment text is too short (lenght {len(comment_data.text)}). Minimum text lenght is 10."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Comment text is too short (lenght {len(comment_data.text)}). Minimum text lenght is 10.",
                )

            query = select(Room).where(Room.unique_code == comment_data.room_code)
            result = await self.session.execute(query)
            room = result.scalars().unique().one_or_none()
            if not room:
                raise HTTPException(
                    status_code=404,
                    detail=f"No room was found with the unique code {comment_data.room_code}.",
                )

            comment_session: Session = await get_session_from_timestamp(
                self.session, comment_data.timestamp, room.id
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
            if room.id != comment_session.room_id:
                logger.error(
                    f"Room unique code {room.id} is not valid for current session."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Room unique code {room.id} is not valid for current session.",
                )

            if not check_location_distance(
                (comment_data.latitude, comment_data.longitude),
                (room.building.latitude, room.building.longitude),
            ):
                raise HTTPException(
                    status_code=404,
                    detail=f"No building was found at users location.",
                )

            ro_timezone = pytz.timezone("Europe/Bucharest")
            if comment_data.timestamp.tzinfo is None:
                comment_data.timestamp = ro_timezone.localize(comment_data.timestamp)
            comment_data.timestamp = comment_data.timestamp.astimezone(pytz.utc)

            new_comment = Comment(
                text=comment_data.text,
                subject_id=comment_session.subject_id,
                timestamp=comment_data.timestamp,
                programme_id=comment_data.programme_id,
                room_id=room.id,
                professor_id=await get_session_professor(
                    self.session, comment_session.subject_id, comment_session.type
                ),
                faculty_id=comment_session.faculty_id,
                session_type=comment_session.type,
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

    async def get_entities_count(self, subject_id: int, session_type: str) -> int:
        try:
            logger.info(
                f"Counting comments for subject with ID {subject_id} with session type {session_type}."
            )
            count_query = (
                select(func.count())
                .select_from(Comment)
                .where(
                    and_(
                        Comment.subject_id == subject_id,
                        Comment.session_type == session_type,
                    )
                )
            )

            result = await self.session.execute(count_query)
            count = result.scalar()
            logger.info(
                f"There are {count} comments for fsubject with ID {subject_id} with session type {session_type}."
            )
            return count
        except Exception as e:
            logger.error(f"An error occurred while counting comments:\n{e}")
            raise HTTPException(
                status_code=500, detail="Could not retrieve comments count."
            )
