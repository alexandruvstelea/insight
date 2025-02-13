from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.faculty import FacultyIn, FacultyOutMinimal
from app.core.database import get_session
from app.core.logging import logger

faculty_router = APIRouter(prefix="/faculty", tags=["faculty"])
