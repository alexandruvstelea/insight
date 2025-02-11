from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import AlchemyAsyncBase
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import Time

if TYPE_CHECKING:
    from subject import Subject
    from room import Room


class Session(AlchemyAsyncBase):
    __tablename__: str = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[str] = mapped_column(nullable=False)
    semester: Mapped[int] = mapped_column(nullable=False)
    week_type: Mapped[int] = mapped_column(nullable=False)
    start: Mapped[Time] = mapped_column(Time, nullable=False)
    end: Mapped[Time] = mapped_column(Time, nullable=False)
    day: Mapped[int] = mapped_column(nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    faculty_id: Mapped[int] = mapped_column(nullable=True)

    # Relationships
    subject: Mapped["Subject"] = relationship(
        "Subject", lazy="subquery", back_populates="sessions"
    )
    room: Mapped["Room"] = relationship(
        "Room", lazy="subquery", back_populates="sessions"
    )
