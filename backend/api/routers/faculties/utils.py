from ...database.models.faculty import Faculty
from .schemas import FacultyOut, FacultyOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


def faculty_to_out(faculty: Faculty) -> FacultyOut:
    from ..buildings.utils import building_to_minimal
    from ..professors.utils import professor_to_minimal
    from ..programmes.utils import programme_to_minimal

    logger.info(f"Converting faculty {faculty.name} to FacultyOut format.")
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
        programmes=(
            [programme_to_minimal(programme) for programme in faculty.programmes]
            if faculty.programmes
            else []
        ),
    )


def faculty_to_minimal(faculty: Faculty) -> FacultyOutMinimal:
    logger.info(f"Converting faculty {faculty.name} to FacultyOutMinimal format.")
    return FacultyOutMinimal(
        id=faculty.id, name=faculty.name, abbreviation=faculty.abbreviation
    )


async def id_to_faculty(session: AsyncSession, faculty_id: int) -> Faculty:
    try:
        logger.info(f"Retrieving faculty for ID {faculty_id}.")
        faculty = await session.get(Faculty, faculty_id)
        if faculty:
            logger.info(f"Retrieved faculty with ID {faculty_id}.")
            return faculty
        logger.error(f"No faculty with ID {faculty_id}.")
        raise HTTPException(status_code=404, detail=f"No faculty with ID {faculty_id}.")
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving faculty with ID {faculty_id}:\n{e}"
        )
        raise e


async def ids_to_faculties(
    session: AsyncSession, faculty_ids: List[int]
) -> List[Faculty]:
    try:
        logger.info(f"Retrieving faculties with IDs {faculty_ids}.")
        result = await session.execute(
            select(Faculty).where(Faculty.id.in_(faculty_ids))
        )
        faculties = result.scalars().all()
        if len(faculties) != len(faculty_ids):
            logger.error(f"One or more faculties not found for IDs {faculty_ids}.")
            raise HTTPException(
                status_code=404,
                detail=f"One or more faculties not found for IDs {faculty_ids}",
            )
        logger.info(f"Retrieved faculties with IDs {faculty_ids}.")
        return list(faculties)
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving faculties with IDs {faculty_ids}:\n{e}"
        )
        raise e
