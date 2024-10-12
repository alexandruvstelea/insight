from ...database.models.ratings import Rating
from .schemas import RatingOut
import logging
import math

logger = logging.getLogger(__name__)


def rating_to_out(rating: Rating):
    if rating:
        logger.info(f"Converting rating {rating} to RatingOut format.")
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
    return None


def check_location_distance(
    rating_location: tuple, building_location_tuple: tuple
) -> bool:
    try:
        logger.info("Calculating distance to building from rating distance.")
        R = 6371000
        lat1, lon1 = rating_location
        lat2, lon2 = building_location_tuple
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance < 150
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while calculating distance:\n{e}"
        )
        raise e
