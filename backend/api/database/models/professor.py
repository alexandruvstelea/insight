from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import List, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, UniqueConstraint

if TYPE_CHECKING:
    from faculty import Faculty
    from subject import Subject


class Professor(AlchemyAsyncBase):
    __tablename__: str = "professors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    faculties_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    faculties: Mapped[List["Faculty"]] = relationship(
        "Faculty",
        secondary="faculties_professors",
        lazy="subquery",
        back_populates="professors",
    )
    courses: Mapped[List["Subject"]] = relationship(
        "Subject",
        lazy="subquery",
        back_populates="course_professor",
        foreign_keys="[Subject.course_professor_id]",
    )
    laboratories: Mapped[List["Subject"]] = relationship(
        "Subject",
        lazy="subquery",
        back_populates="laboratory_professor",
        foreign_keys="[Subject.laboratory_professor_id]",
    )
    seminars: Mapped[List["Subject"]] = relationship(
        "Subject",
        lazy="subquery",
        back_populates="seminar_professor",
        foreign_keys="[Subject.seminar_professor_id]",
    )
    projects: Mapped[List["Subject"]] = relationship(
        "Subject",
        lazy="subquery",
        back_populates="project_professor",
        foreign_keys="[Subject.project_professor_id]",
    )
    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="unique_first_last_name"),
    )
