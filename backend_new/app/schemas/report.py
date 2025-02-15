from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReportBase(BaseModel):
    text: str
    timestamp: datetime


class ReportIn(ReportBase):
    pass


class ReportOutMinimal(ReportBase):
    id: int


class ReportOut(ReportBase):
    id: int

    class Config:
        from_attributes = True


class ReportFilter(BaseModel):
    timestamp_after: Optional[datetime] = None
    timestamp_before: Optional[datetime] = None
