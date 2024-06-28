from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.sql.sqltypes import Time
from sqlalchemy.dialects.postgresql import ARRAY

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
    faculties_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    subject: Mapped["Subject"] = relationship(
        "Subject", lazy="subquery", back_populates="sessions"
    )
    room: Mapped["Room"] = relationship(
        "Room", lazy="subquery", back_populates="sessions"
    )
