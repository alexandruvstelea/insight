from __future__ import annotations
from pydantic import BaseModel
from typing import Literal, Optional


class UserBase(BaseModel):
    email: str
    password: str
    role: Literal["admin", "professor", "student"]
    professor_id: Optional[int] = None


class UserIn(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    role: Literal["admin", "professor", "student"]
    professor_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserFilter(BaseModel):
    email: Optional[str] = None
    role: Optional[Literal["admin", "professor", "student"]] = None
    professor_id: Optional[int] = None
