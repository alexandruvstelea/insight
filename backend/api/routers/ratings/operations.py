from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.ratings import Rating
from .schemas import RatingOut, RatingIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import rating_to_out


class RatingOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ratings(
        self, professor_id: int, subject_id: int, session_type: str
    ) -> List[RatingOut]:
        try:
            raise HTTPException(status_code=404, detail="No sessions found.")
        except Exception as e:
            raise e

    async def add_rating(self, rating_data: RatingIn) -> RatingOut:
        try:
            new_rating = Rating(
                rating_clarity=rating_data.rating_clarity,
                rating_interactivity=rating_data.rating_interactivity,
                ratint_relevance=rating_data.rating_relevance,
                rating_comprehension=rating_data.rating_comprehension,
                rating_overall=(
                    rating_data.rating_clarity
                    + rating_data.rating_interactivity
                    + rating_data.rating_relevance
                    + rating_data.rating_comprehension
                )
                / 4,
                timestamp=rating_data.timestamp,
            )

            self.session.add(new_rating)
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
