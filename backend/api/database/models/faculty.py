from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from building import Building
    from programme import Programme


class Faculty(AlchemyAsyncBase):
    __tablename__: str = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    abbreviation: Mapped[str] = mapped_column(unique=True)
    programmes: Mapped[List["Programme"]] = relationship(
        "Programme", lazy="subquery", back_populates="faculty"
    )
    buildings: Mapped[List["Building"]] = relationship(
        "Building",
        secondary="faculties_buildings",
        lazy="subquery",
        back_populates="faculties",
    )
