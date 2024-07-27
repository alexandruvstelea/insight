from ...database.models.comments import Comment
from .schemas import CommentOut
import logging

logger = logging.getLogger(__name__)


def comment_to_out(comment: Comment) -> CommentOut:
    logger.info(f"Converting comment {comment} to CommentOut format.")
    return CommentOut(
        id=comment.id,
        text=comment.text,
        timestamp=comment.timestamp,
        room_id=comment.room_id,
        programme_id=comment.programme_id,
        professor_id=comment.professor_id,
        faculty_id=comment.faculty_id,
        subject_id=comment.subject_id,
    )
