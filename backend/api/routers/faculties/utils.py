from ...database.models.faculty import Faculty
from .schemas import FacultyOut, FacultyOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def faculty_to_out(faculty: Faculty) -> FacultyOut:
    from ..buildings.utils import building_to_minimal
    from ..professors.utils import professor_to_minimal

    return FacultyOut(
        id=faculty.id,
        name=faculty.name,
        abbreviation=faculty.abbreviation,
        buildings=(
            [building_to_minimal(building) for building in faculty.buildings]
            if faculty.buildings
            else []
        ),
        professors=(
            [professor_to_minimal(professor) for professor in faculty.professors]
            if faculty.professors
            else []
        ),
    )


def faculty_to_minimal(faculty: Faculty) -> FacultyOutMinimal:
    return FacultyOutMinimal(
        id=faculty.id, name=faculty.name, abbreviation=faculty.abbreviation
    )


async def id_to_faculty(session: AsyncSession, faculty_id: int) -> Faculty:
    faculty = await session.get(Faculty, faculty_id)
    if faculty:
        return faculty
    raise HTTPException(status_code=404, detail=f"No faculty with id={faculty_id}.")


async def ids_to_faculties(
    session: AsyncSession, faculty_ids: List[int]
) -> List[Faculty]:
    result = await session.execute(select(Faculty).where(Faculty.id.in_(faculty_ids)))
    faculties = result.scalars().all()
    if len(faculties) != len(faculty_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more faculties not found for IDs {faculty_ids}",
        )
    return list(faculties)
