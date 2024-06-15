from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from faculty import Faculty


class Programme(AlchemyAsyncBase):
    __tablename__: str = "programmes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    abbreviation: Mapped[str] = mapped_column(unique=True)
    type: Mapped[int] = mapped_column()
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"))
    faculty: Mapped["Faculty"] = relationship(
        "Faculty", lazy="subquery", back_populates="programmes"
    )
