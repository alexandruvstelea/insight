from ...database.models.ratings import Rating
from ...database.models.session import Session
from .schemas import RatingOut
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def rating_to_out(rating: Rating):
    return RatingOut(
        id=rating.id,
        rating_clarity=rating.rating_clarity,
        rating_interactivity=rating.rating_interactivity,
        rating_relevance=rating.rating_relevance,
        rating_comprehension=rating.rating_comprehension,
        rating_overall=rating.rating_overall,
        timestamp=rating.timestamp,
        session_type=rating.session_type,
        subject_id=rating.subject_id,
        programme_id=rating.programme_id,
        room_id=rating.room_id,
        professor_id=rating.professor_id,
        faculty_id=rating.faculty_id,
    )
