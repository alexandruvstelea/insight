from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from app.core.database import AlchemyAsyncBase

Base = declarative_base()


class VoteLimiter(AlchemyAsyncBase):
    __tablename__ = "vote_limiter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=False, index=True)
    time_slot: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(now() at time zone 'utc')"),
    )
