from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List, Literal, Optional


class WeekBase(BaseModel):
    start: date
    end: date
    semester: Literal[1, 2]


class WeekIn(BaseModel):
    year_start: date
    intervals: List[int] = Field(..., min_items=8, max_items=8)

    @field_validator("intervals")
    def check_intervals_length(cls, v):
        if len(v) != 8:
            raise ValueError("Intervals must have exactly 8 items")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "year_start": "2023-10-02",
                "intervals": [12, 2, 2, 3, 1, 10, 1, 4],
            }
        }


class WeekOut(WeekBase):
    id: int

    class Config:
        from_attributes = True


class WeekFilter(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None
    semester: Optional[Literal[1, 2]] = None
