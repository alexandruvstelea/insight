from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY


if TYPE_CHECKING:
    from building import Building
    from session import Session


class Room(AlchemyAsyncBase):
    __tablename__: str = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    faculties_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    building: Mapped["Building"] = relationship(
        "Building", lazy="subquery", back_populates="rooms"
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session", lazy="subquery", back_populates="room"
    )
