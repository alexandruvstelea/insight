from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.ratings import Rating
from ...database.models.session import Session
from .schemas import RatingOut, RatingIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import rating_to_out
from ..sessions.utils import get_session_from_timestamp
from ..subjects.utils import get_subject_session_professor


class RatingOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ratings(
        self, professor_id: int, subject_id: int, session_type: str
    ) -> List[RatingOut]:
        try:
            raise HTTPException(status_code=404, detail="No ratings found.")
        except Exception as e:
            raise e

    async def add_rating(self, rating_data: RatingIn) -> RatingOut:
        try:
            rating_session: Session = await get_session_from_timestamp(
                self.session, rating_data.timestamp, rating_data.room_id
            )
            new_rating = Rating(
                rating_clarity=rating_data.rating_clarity,
                rating_interactivity=rating_data.rating_interactivity,
                rating_relevance=rating_data.rating_relevance,
                rating_comprehension=rating_data.rating_comprehension,
                rating_overall=(
                    rating_data.rating_clarity
                    + rating_data.rating_interactivity
                    + rating_data.rating_relevance
                    + rating_data.rating_comprehension
                )
                / 4,
                timestamp=rating_data.timestamp,
                session_type=rating_session.type,
                subject_id=rating_session.subject_id,
                programme_id=rating_data.programme_id,
                room_id=rating_data.room_id,
                professor_id=await get_subject_session_professor(
                    self.session, rating_session.subject_id, rating_session.type
                ),
                faculty_id=rating_session.faculty_id,
            )

            self.session.add(new_rating)
            print(new_rating.professor_id)
            await self.session.commit()
            await self.session.refresh(new_rating)
            return rating_to_out(new_rating)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e
