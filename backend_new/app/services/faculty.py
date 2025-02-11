from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.faculty import FacultyIn, FacultyOutMinimal
from app.repositories.implementations.faculty_repository import FacultyRepository
from app.core.logging import logger


async def create_new_faculty(
    db: AsyncSession, faculty_data: FacultyIn
) -> FacultyOutMinimal | None:
    new_faculty = FacultyRepository.create(faculty_data)
    return FacultyOutMinimal.model_validate(new_faculty)


async def get_all_facultiess(db: AsyncSession) -> list[FacultyOutMinimal] | None:
    faculties = await FacultyRepository.get_all()
    if faculties:
        return faculties
    return None
