from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.faculty import FacultyIn, FacultyOutMinimal
from app.services.faculty import create_new_faculty, get_all_facultiess
from app.core.database import get_session
from app.core.logging import logger

faculty_router = APIRouter(prefix="/faculty", tags=["faculty"])


@faculty_router.post("/", response_model=FacultyOutMinimal | None)
async def create_faculty(faculty: FacultyIn, db: AsyncSession = Depends(get_session)):
    return await create_new_faculty(db, faculty)


@faculty_router.get("/", response_model=list[FacultyOutMinimal] | None)
async def get_faculties(db: AsyncSession = Depends(get_session)):
    return await get_all_facultiess(db)
