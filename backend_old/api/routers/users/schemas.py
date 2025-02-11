from __future__ import annotations
from pydantic import BaseModel
from typing import Literal, Optional


class UserBase(BaseModel):
    email: str
    password: str
    role: Literal["admin", "professor", "student", "tablet"]
    professor_id: Optional[int] = None


class UserIn(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    role: Literal["admin", "professor", "student", "tablet"]
    professor_id: Optional[int] = None
