from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from faculty import Faculty


class Building(AlchemyAsyncBase):
    __tablename__: str = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    faculties: Mapped[List["Faculty"]] = relationship(
        "Faculty",
        secondary="faculties_buildings",
        lazy="subquery",
        back_populates="buildings",
    )
