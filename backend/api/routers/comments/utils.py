from ...database.models.comments import Comment
from .schemas import CommentOut
import logging
import pytz

logger = logging.getLogger(__name__)


def comment_to_out(comment: Comment) -> CommentOut:
    if comment:
        logger.info(f"Converting comment with ID {comment.id} to CommentOut format.")
        ro_timezone = pytz.timezone("Europe/Bucharest")
        if comment.timestamp.tzinfo is None:
            comment.timestamp = pytz.utc.localize(comment.timestamp)
        timestamp_ro = comment.timestamp.astimezone(ro_timezone)
        return CommentOut(
            id=comment.id,
            text=comment.text,
            timestamp=timestamp_ro,
            room_id=comment.room_id,
            programme_id=comment.programme_id,
            professor_id=comment.professor_id,
            faculty_id=comment.faculty_id,
            subject_id=comment.subject_id,
            session_type=comment.session_type,
        )
    return None
