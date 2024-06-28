from ...database.models.subject import Subject
from .schemas import SubjectOut, SubjectOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def subject_to_out(subject: Subject) -> SubjectOut:
    from ..programmes.utils import programme_to_minimal
    from ..sessions.utils import session_to_minimal
    from ..professors.utils import professor_to_minimal

    return SubjectOut(
        id=subject.id,
        name=subject.name,
        abbreviation=subject.abbreviation,
        semester=subject.semester,
        course_professor_id=subject.course_professor_id,
        laboratory_professor_id=subject.laboratory_professor_id,
        seminar_professor_id=subject.seminar_professor_id,
        project_professor_id=subject.project_professor_id,
        programmes=(
            [programme_to_minimal(programme) for programme in subject.programmes]
            if subject.programmes
            else []
        ),
        sessions=(
            [session_to_minimal(session) for session in subject.sessions]
            if subject.sessions
            else []
        ),
        course_professor=(
            professor_to_minimal(subject.course_professor)
            if subject.course_professor_id
            else None
        ),
        laboratory_professor=(
            professor_to_minimal(subject.laboratory_professor)
            if subject.laboratory_professor_id
            else None
        ),
        seminar_professor=(
            professor_to_minimal(subject.seminar_professor)
            if subject.seminar_professor_id
            else None
        ),
        project_professor=(
            professor_to_minimal(subject.project_professor)
            if subject.project_professor_id
            else None
        ),
    )


def subject_to_minimal(subject: Subject) -> SubjectOutMinimal:
    return SubjectOutMinimal(
        id=subject.id,
        name=subject.name,
        abbreviation=subject.abbreviation,
        semester=subject.semester,
        course_professor_id=subject.course_professor_id,
        laboratory_professor_id=subject.laboratory_professor_id,
        seminar_professor_id=subject.seminar_professor_id,
        project_professor_id=subject.project_professor_id,
    )


async def id_to_subject(session: AsyncSession, subject_id: int) -> Subject:
    subject = await session.get(Subject, subject_id)
    if subject:
        return subject
    raise HTTPException(status_code=404, detail=f"No subject with id={subject_id}.")


async def ids_to_subjects(
    session: AsyncSession, subject_ids: List[int]
) -> List[Subject]:
    result = await session.execute(select(Subject).where(Subject.id.in_(subject_ids)))
    subjects = result.scalars().all()
    if len(subjects) != len(subject_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more professors not found for IDs {subject_ids}",
        )
    return list(subjects)


async def get_subject_semester(session: AsyncSession, subject_id: int) -> int:
    result = await session.execute(
        select(Subject.semester).where(Subject.id == subject_id)
    )
    subject_semester = result.scalars().first()
    return subject_semester
