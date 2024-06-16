from ...database.models.professor import Professor
from .schemas import ProfessorOut, ProfessorOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def professor_to_out(professor: Professor) -> ProfessorOut:
    from ..faculties.utils import faculty_to_minimal

    return ProfessorOut(
        id=professor.id,
        first_name=professor.first_name,
        last_name=professor.last_name,
        gender=professor.gender,
        faculties=(
            [faculty_to_minimal(faculty) for faculty in professor.faculties]
            if professor.faculties
            else []
        ),
    )


def professor_to_minimal(professor: Professor) -> ProfessorOutMinimal:
    return ProfessorOutMinimal(
        id=professor.id,
        first_name=professor.first_name,
        last_name=professor.last_name,
        gender=professor.gender,
    )


async def id_to_professor(session: AsyncSession, professor_id: int) -> Professor:
    professor = await session.get(Professor, professor_id)
    if professor:
        return professor
    raise HTTPException(status_code=404, detail=f"No professor with id={professor_id}.")


async def ids_to_professors(
    session: AsyncSession, professor_ids: List[int]
) -> List[Professor]:
    result = await session.execute(
        select(Professor).where(Professor.id.in_(professor_ids))
    )
    professors = result.scalars().all()
    if len(professors) != len(professor_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more professors not found for IDs {professor_ids}",
        )
    return list(professors)
