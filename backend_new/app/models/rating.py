from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import AlchemyAsyncBase
from sqlalchemy import ForeignKey, text
from sqlalchemy.sql.sqltypes import DateTime


class Rating(AlchemyAsyncBase):
    __tablename__: str = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    rating_clarity: Mapped[int] = mapped_column(nullable=False)
    rating_interactivity: Mapped[int] = mapped_column(nullable=False)
    rating_relevance: Mapped[int] = mapped_column(nullable=False)
    rating_comprehension: Mapped[int] = mapped_column(nullable=False)
    rating_overall: Mapped[float] = mapped_column(nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(now() at time zone 'utc')"),
    )
    session_type: Mapped[str] = mapped_column(nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    programme_id: Mapped[int] = mapped_column(
        ForeignKey("programmes.id"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professors.id"), nullable=False
    )
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
