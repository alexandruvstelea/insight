from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY


if TYPE_CHECKING:
    from building import Building
    from session import Session


class Room(AlchemyAsyncBase):
    __tablename__: str = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=True)
    faculties_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    unique_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    building: Mapped["Building"] = relationship(
        "Building", lazy="subquery", back_populates="rooms"
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session", lazy="subquery", back_populates="room"
    )
