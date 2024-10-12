from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class ReportBase(BaseModel):
    text: str
    timestamp: datetime


class ReportIn(ReportBase):
    pass


class ReportOutMinimal(ReportBase):
    id: int


class ReportOut(ReportBase):
    id: int
