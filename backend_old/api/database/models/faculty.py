from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from building import Building
    from programme import Programme
    from professor import Professor


class Faculty(AlchemyAsyncBase):
    __tablename__: str = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    abbreviation: Mapped[str] = mapped_column(unique=True, nullable=False)
    programmes: Mapped[List["Programme"]] = relationship(
        "Programme", lazy="subquery", back_populates="faculty"
    )
    buildings: Mapped[List["Building"]] = relationship(
        "Building",
        secondary="faculties_buildings",
        lazy="subquery",
        back_populates="faculties",
    )
    professors: Mapped[List["Professor"]] = relationship(
        "Professor",
        secondary="faculties_professors",
        lazy="subquery",
        back_populates="faculties",
    )
