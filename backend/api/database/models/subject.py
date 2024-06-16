from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from programme import Programme


class Subject(AlchemyAsyncBase):
    __tablename__: str = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    abbreviation: Mapped[str] = mapped_column(unique=True)
    semester: Mapped[int] = mapped_column()
    course_professor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("professors.id"), nullable=True
    )
    laboratory_professor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("professors.id"), nullable=True
    )
    seminar_professor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("professors.id"), nullable=True
    )
    project_professor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("professors.id"), nullable=True
    )
    programmes: Mapped[List["Programme"]] = relationship(
        "Programme",
        secondary="programmes_subjects",
        lazy="subquery",
        back_populates="subjects",
    )
