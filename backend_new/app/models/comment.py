from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import text as txt
from app.core.database import AlchemyAsyncBase
from sqlalchemy.sql.sqltypes import DateTime


class Comment(AlchemyAsyncBase):
    __tablename__: str = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=txt("(now() at time zone 'utc')"),
    )
    programme_id: Mapped[int] = mapped_column(
        ForeignKey("programmes.id"), nullable=True
    )
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=True)
    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professors.id"), nullable=True
    )
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=True)
    session_type: Mapped[str] = mapped_column(nullable=False)
