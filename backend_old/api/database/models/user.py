from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..main import AlchemyAsyncBase
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import Time

if TYPE_CHECKING:
    from subject import Subject
    from room import Room


class User(AlchemyAsyncBase):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professors.id"), unique=True, nullable=True
    )
