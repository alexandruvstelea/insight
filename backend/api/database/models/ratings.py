from sqlalchemy.orm import Mapped, mapped_column
from ..main import AlchemyAsyncBase
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


class Rating(AlchemyAsyncBase):
    __tablename__: str = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    rating_clarity: Mapped[int] = mapped_column()
    rating_interactivity: Mapped[int] = mapped_column()
    rating_relevance: Mapped[int] = mapped_column()
    rating_comprehension: Mapped[int] = mapped_column()
    rating_overall: Mapped[float] = mapped_column()
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
    session_type: Mapped[str] = mapped_column()
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professors.id"))
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"))
