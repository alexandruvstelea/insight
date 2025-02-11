from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import AlchemyAsyncBase
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import text as txt


class Report(AlchemyAsyncBase):
    __tablename__: str = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=txt("(now() at time zone 'utc')"),
    )
