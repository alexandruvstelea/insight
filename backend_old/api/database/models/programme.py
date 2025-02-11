from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from faculty import Faculty
    from subject import Subject


class Programme(AlchemyAsyncBase):
    __tablename__: str = "programmes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    abbreviation: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=True)
    faculty: Mapped["Faculty"] = relationship(
        "Faculty", lazy="subquery", back_populates="programmes"
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        secondary="programmes_subjects",
        lazy="subquery",
        back_populates="programmes",
    )
