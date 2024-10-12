from sqlalchemy.orm import Mapped, mapped_column
from ..main import AlchemyAsyncBase
from sqlalchemy.sql.sqltypes import DateTime


class Report(AlchemyAsyncBase):
    __tablename__: str = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
