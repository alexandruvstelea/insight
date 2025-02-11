from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import AlchemyAsyncBase
from sqlalchemy.sql.sqltypes import Date


class Week(AlchemyAsyncBase):
    __tablename__: str = "weeks"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    start: Mapped[Date] = mapped_column(Date, nullable=False)
    end: Mapped[Date] = mapped_column(Date, nullable=False)
    semester: Mapped[int] = mapped_column(nullable=False)
