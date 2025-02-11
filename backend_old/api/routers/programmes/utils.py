from ...database.models.programme import Programme
from .schemas import ProgrammeOut, ProgrammeOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


def programme_to_out(programme: Programme) -> ProgrammeOut:
    from ..faculties.utils import faculty_to_minimal
    from ..subjects.utils import subject_to_minimal
    if programme:
        logger.info(f"Converting programme {programme.name} to ProgrammeOut format.")
        return ProgrammeOut(
            id=programme.id,
            name=programme.name,
            type=programme.type,
            abbreviation=programme.abbreviation,
            faculty=faculty_to_minimal(programme.faculty),
            subjects=[subject_to_minimal(subject) for subject in programme.subjects],
        )
    return None

def programme_to_minimal(programme: Programme) -> ProgrammeOutMinimal:
    if programme:
        logger.info(f"Converting programme {programme.name} to ProgrammeOutMinimal format.")
        return ProgrammeOutMinimal(
            id=programme.id,
            name=programme.name,
            abbreviation=programme.abbreviation,
            type=programme.type,
        )
    return None

async def id_to_programme(session: AsyncSession, programme_id: int) -> Programme:
    try:
        if programme_id:
            logger.info(f"Retrieving programme for ID {programme_id}.")
            programme = await session.get(Programme, programme_id)
            if programme:
                logger.info(f"Retrieved programme with ID {programme_id}.")
                return programme
            logger.error(f"No programme with ID {programme_id}.")
            raise HTTPException(
                status_code=404, detail=f"No programme with id={programme_id}."
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving programme with ID {programme_id}:\n{e}"
        )
        raise e


async def ids_to_programmes(
    session: AsyncSession, programme_ids: List[int]
) -> List[Programme]:
    try:
        if programme_ids:
            logger.info(f"Retrieving programmes with IDs {programme_ids}.")
            result = await session.execute(
                select(Programme).where(Programme.id.in_(programme_ids))
            )
            programmes = result.scalars().all()
            if len(programmes) != len(programme_ids):
                logger.error(f"One or more programmes not found for IDs {programme_ids}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"One or more programmes not found for IDs {programme_ids}",
                )
            logger.info(f"Retrieved programmes with IDs {programme_ids}.")
            return list(programmes)
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving programmes with IDs {programme_ids}:\n{e}"
        )
        raise e
