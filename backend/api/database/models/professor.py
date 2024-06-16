from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from faculty import Faculty
    from programme import Programme


class Professor(AlchemyAsyncBase):
    __tablename__: str = "professors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column(unique=True)
    gender: Mapped[int] = mapped_column()
    faculties: Mapped[List["Faculty"]] = relationship(
        "Faculty",
        secondary="faculties_professors",
        lazy="subquery",
        back_populates="professors",
    )
