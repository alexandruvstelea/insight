from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from building import Building


class Faculty(AlchemyAsyncBase):
    __tablename__: str = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    abbreviation: Mapped[str] = mapped_column(unique=True)
    buildings: Mapped[List["Building"]] = relationship(
        "Building",
        secondary="faculties_buildings",
        lazy="subquery",
        back_populates="faculties",
    )
