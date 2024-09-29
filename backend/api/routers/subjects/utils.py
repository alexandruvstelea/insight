from ...database.models.subject import Subject
from .schemas import SubjectOut, SubjectOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


def subject_to_out(subject: Subject) -> SubjectOut:
    from ..programmes.utils import programme_to_minimal
    from ..sessions.utils import session_to_minimal
    from ..professors.utils import professor_to_minimal

    if subject:
        logger.info(f"Converting subject {subject.name} to SubjectOut format.")
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
    return None


def subject_to_minimal(subject: Subject) -> SubjectOutMinimal:
    if subject:
        logger.info(f"Converting subject {subject.name} to SubjectOutMinimal format.")
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
    return None


async def id_to_subject(session: AsyncSession, subject_id: int) -> Subject:
    try:
        if subject_id:
            logger.info(f"Retrieving subject for ID {subject_id}.")
            subject = await session.get(Subject, subject_id)
            if subject:
                logger.info(f"Retrieved subject with ID {subject_id}.")
                return subject
            logger.error(f"No subject with ID {subject_id}.")
            raise HTTPException(
                status_code=404, detail=f"No subject with id={subject_id}."
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving subject with ID {subject_id}:\n{e}"
        )
        raise e


async def ids_to_subjects(
    session: AsyncSession, subject_ids: List[int]
) -> List[Subject]:
    try:
        if subject_ids:
            logger.info(f"Retrieving subjects for IDs {subject_ids}.")
            result = await session.execute(
                select(Subject).where(Subject.id.in_(subject_ids))
            )
            subjects = result.scalars().all()
            if len(subjects) != len(subject_ids):
                logger.error(f"One or more subjects not found for IDs {subject_ids}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"One or more professors not found for IDs {subject_ids}",
                )
            logger.info(f"Retrieved subjects with IDs {subject_ids}.")
            return list(subjects)
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving subjects with IDs {subject_ids}:\n{e}"
        )
        raise e


async def get_subject_semester(session: AsyncSession, subject_id: int) -> int:
    try:
        if subject_id:
            logger.info(f"Retrieving semester of subject with ID {subject_id}.")
            result = await session.execute(
                select(Subject.semester).where(Subject.id == subject_id)
            )
            subject_semester = result.scalars().first()
            if subject_semester:
                logger.info(
                    f"Retrieved semester {subject_semester} for subject with ID {subject_id}."
                )
                return subject_semester
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving semester of subject with ID {subject_id}:\n{e}"
        )
        raise e


async def get_session_professor(
    session: AsyncSession, subject_id: int, type: str
) -> int:
    try:
        if subject_id and type:
            logger.info(
                f"Retrieving {type} professor for subject with ID {subject_id}."
            )
            subject: Subject = await id_to_subject(session, subject_id)
            match type:
                case "course":
                    return subject.course_professor_id
                case "laboratory":
                    return subject.laboratory_professor_id
                case "seminar":
                    return subject.seminar_professor_id
                case "project":
                    return subject.project_professor_id
                case _:
                    logger.error(
                        f"Could not find {type} professor for subject {subject.name}."
                    )
                    raise HTTPException(
                        status_code=404,
                        detail=f"Could not find {type} professor for subject {subject.name}.",
                    )
            return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving {type} professor for subject with ID {subject_id}:\n{e}"
        )
        raise e
