from sqlalchemy.orm import Mapped, mapped_column
from ..main import AlchemyAsyncBase
from sqlalchemy.sql.sqltypes import Date


class Week(AlchemyAsyncBase):
    __tablename__: str = "weeks"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    start: Mapped[Date] = mapped_column(Date)
    end: Mapped[Date] = mapped_column(Date)
    semester: Mapped[int] = mapped_column()
