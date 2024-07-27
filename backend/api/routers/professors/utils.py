from ...database.models.professor import Professor
from .schemas import ProfessorOut, ProfessorOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


def professor_to_out(professor: Professor) -> ProfessorOut:
    from ..faculties.utils import faculty_to_minimal
    from ..subjects.utils import subject_to_minimal

    logger.info(
        f"Converting professor {professor.first_name} {professor.last_name} to ProfessorOut format."
    )
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
        courses=(
            [subject_to_minimal(course) for course in professor.courses]
            if professor.courses
            else []
        ),
        laboratories=(
            [subject_to_minimal(laboratory) for laboratory in professor.laboratories]
            if professor.laboratories
            else []
        ),
        seminars=(
            [subject_to_minimal(seminar) for seminar in professor.seminars]
            if professor.seminars
            else []
        ),
        projects=(
            [subject_to_minimal(project) for project in professor.projects]
            if professor.projects
            else []
        ),
    )


def professor_to_minimal(professor: Professor) -> ProfessorOutMinimal:
    logger.info(
        f"Converting professor {professor.first_name} {professor.last_name} to ProfessorOutMinimal format."
    )
    return ProfessorOutMinimal(
        id=professor.id,
        first_name=professor.first_name,
        last_name=professor.last_name,
        gender=professor.gender,
    )


async def id_to_professor(session: AsyncSession, professor_id: int) -> Professor:
    try:
        logger.info(f"Retrieving professor for ID {professor_id}.")
        professor = await session.get(Professor, professor_id)
        if professor:
            logger.info(f"Retrieved professor with ID {professor_id}.")
            return professor
        logger.error(f"No professor with ID {professor_id}.")
        raise HTTPException(
            status_code=404, detail=f"No professor with id={professor_id}."
        )
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving professor with ID {professor_id}:\n{e}"
        )
        raise e


async def ids_to_professors(
    session: AsyncSession, professor_ids: List[int]
) -> List[Professor]:
    try:
        logger.info(f"Retrieving professors with IDs {professor_ids}.")
        result = await session.execute(
            select(Professor).where(Professor.id.in_(professor_ids))
        )
        professors = result.scalars().all()
        if len(professors) != len(professor_ids):
            logger.error(f"One or more professors not found for IDs {professor_ids}.")
            raise HTTPException(
                status_code=404,
                detail=f"One or more professors not found for IDs {professor_ids}",
            )
        logger.info(f"Retrieved professors with IDs {professor_ids}.")
        return list(professors)
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving professors with IDs {professor_ids}:\n{e}"
        )
        raise e
