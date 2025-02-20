from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import AlchemyAsyncBase
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY

if TYPE_CHECKING:
    from programme import Programme
    from session import Session
    from professor import Professor


class Subject(AlchemyAsyncBase):
    __tablename__: str = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    abbreviation: Mapped[str] = mapped_column(unique=True, nullable=False)
    semester: Mapped[int] = mapped_column(nullable=False)
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

    # Relationships
    programmes: Mapped[List["Programme"]] = relationship(
        "Programme",
        secondary="programmes_subjects",
        lazy="subquery",
        back_populates="subjects",
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session", lazy="subquery", back_populates="subject"
    )
    course_professor: Mapped["Professor"] = relationship(
        "Professor",
        lazy="subquery",
        back_populates="courses",
        foreign_keys="[Subject.course_professor_id]",
    )
    laboratory_professor: Mapped["Professor"] = relationship(
        "Professor",
        lazy="subquery",
        back_populates="laboratories",
        foreign_keys="[Subject.laboratory_professor_id]",
    )
    seminar_professor: Mapped["Professor"] = relationship(
        "Professor",
        lazy="subquery",
        back_populates="seminars",
        foreign_keys="[Subject.seminar_professor_id]",
    )
    project_professor: Mapped["Professor"] = relationship(
        "Professor",
        lazy="subquery",
        back_populates="projects",
        foreign_keys="[Subject.project_professor_id]",
    )
