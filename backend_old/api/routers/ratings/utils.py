from ...database.models.ratings import Rating
from .schemas import RatingOut
import logging
import pytz

logger = logging.getLogger(__name__)


def rating_to_out(rating: Rating):
    if rating:
        logger.info(f"Converting rating to RatingOut format.")
        ro_timezone = pytz.timezone("Europe/Bucharest")
        if rating.timestamp.tzinfo is None:
            rating.timestamp = pytz.utc.localize(rating.timestamp)
        timestamp_ro = rating.timestamp.astimezone(ro_timezone)

        return RatingOut(
            id=rating.id,
            rating_clarity=rating.rating_clarity,
            rating_interactivity=rating.rating_interactivity,
            rating_relevance=rating.rating_relevance,
            rating_comprehension=rating.rating_comprehension,
            rating_overall=rating.rating_overall,
            timestamp=timestamp_ro,
            session_type=rating.session_type,
            subject_id=rating.subject_id,
            programme_id=rating.programme_id,
            room_id=rating.room_id,
            professor_id=rating.professor_id,
            faculty_id=rating.faculty_id,
        )
    return None
