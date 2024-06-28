from ...database.models.programme import Programme
from .schemas import ProgrammeOut, ProgrammeOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def programme_to_out(programme: Programme) -> ProgrammeOut:
    from ..faculties.utils import faculty_to_minimal
    from ..subjects.utils import subject_to_minimal

    return ProgrammeOut(
        id=programme.id,
        name=programme.name,
        type=programme.type,
        abbreviation=programme.abbreviation,
        faculty=faculty_to_minimal(programme.faculty),
        subjects=[subject_to_minimal(subject) for subject in programme.subjects],
    )


def programme_to_minimal(programme: Programme) -> ProgrammeOutMinimal:
    return ProgrammeOutMinimal(
        id=programme.id,
        name=programme.name,
        abbreviation=programme.abbreviation,
        type=programme.type,
    )


async def id_to_programme(session: AsyncSession, programme_id: int) -> Programme:
    programme = await session.get(Programme, programme_id)
    if programme:
        return programme
    raise HTTPException(status_code=404, detail=f"No programme with id={programme_id}.")


async def ids_to_programmes(
    session: AsyncSession, programme_ids: List[int]
) -> List[Programme]:
    result = await session.execute(
        select(Programme).where(Programme.id.in_(programme_ids))
    )
    programmes = result.scalars().all()
    if len(programmes) != len(programme_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more programmes not found for IDs {programme_ids}",
        )
    return list(programmes)
