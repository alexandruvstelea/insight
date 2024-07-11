from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import Time

if TYPE_CHECKING:
    from subject import Subject
    from room import Room


class Session(AlchemyAsyncBase):
    __tablename__: str = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[str] = mapped_column()
    semester: Mapped[int] = mapped_column()
    week_type: Mapped[int] = mapped_column()
    start: Mapped[Time] = mapped_column(Time)
    end: Mapped[Time] = mapped_column(Time)
    day: Mapped[int] = mapped_column()
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    faculty_id: Mapped[int] = mapped_column()
    subject: Mapped["Subject"] = relationship(
        "Subject", lazy="subquery", back_populates="sessions"
    )
    room: Mapped["Room"] = relationship(
        "Room", lazy="subquery", back_populates="sessions"
    )
