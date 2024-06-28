from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload
from ...database.models.subject import Subject
from .schemas import SubjectOut, SubjectIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import subject_to_out
from ..programmes.utils import id_to_programme, ids_to_programmes
from ..sessions.utils import ids_to_sessions
from ..professors.utils import id_to_professor


class SubjectOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_subjects(
        self, faculty_id: int, professor_id: int
    ) -> List[SubjectOut]:
        try:
            if faculty_id and not professor_id:
                query = (
                    select(Subject)
                    .options(joinedload(Subject.programmes))
                    .where(Subject.faculties_ids.contains([faculty_id]))
                )
            elif professor_id and not faculty_id:
                query = (
                    select(Subject)
                    .options(joinedload(Subject.programmes))
                    .where(
                        or_(
                            Subject.course_professor_id == professor_id,
                            Subject.laboratory_professor_id == professor_id,
                            Subject.project_professor_id == professor_id,
                            Subject.seminar_professor_id == professor_id,
                        ),
                    )
                )
            elif professor_id and faculty_id:
                query = (
                    select(Subject)
                    .options(joinedload(Subject.programmes))
                    .where(
                        and_(
                            or_(
                                Subject.course_professor_id == professor_id,
                                Subject.laboratory_professor_id == professor_id,
                                Subject.project_professor_id == professor_id,
                                Subject.seminar_professor_id == professor_id,
                            ),
                            Subject.faculties_ids.contains([faculty_id]),
                        )
                    )
                )
            else:
                query = select(Subject).options(joinedload(Subject.programmes))
            result = await self.session.execute(query)
            subjects = result.scalars().unique().all()
            if subjects:
                return [
                    subject_to_out(room)
                    for room in sorted(list(subjects), key=lambda x: x.name)
                ]
            raise HTTPException(status_code=404, detail="No subjects found.")
        except Exception as e:
            raise e

    async def get_subject_by_id(self, id: int) -> SubjectOut:
        subject = await self.session.get(Subject, id)
        try:
            if subject:
                return subject_to_out(subject)
            raise HTTPException(status_code=404, detail=f"No subject with id={id}.")
        except Exception as e:
            raise e

    async def add_subject(self, subject_data: SubjectIn) -> SubjectOut:
        try:
            new_subject = Subject(
                name=subject_data.name,
                abbreviation=subject_data.abbreviation.upper(),
                semester=subject_data.semester,
                course_professor_id=subject_data.course_professor_id,
                laboratory_professor_id=subject_data.laboratory_professor_id,
                seminar_professor_id=subject_data.seminar_professor_id,
                project_professor_id=subject_data.project_professor_id,
                programmes=[],
            )
            if subject_data.programmes:
                new_subject.programmes = [
                    await id_to_programme(self.session, programme)
                    for programme in subject_data.programmes
                ]
                new_subject.faculties_ids = list(
                    set(programme.faculty_id for programme in new_subject.programmes)
                )
            if subject_data.sessions:
                new_subject.sessions = await ids_to_sessions(
                    self.session, subject_data.sessions
                )
            if subject_data.course_professor_id:
                new_subject.course_professor = await id_to_professor(
                    self.session, subject_data.course_professor_id
                )
            if subject_data.laboratory_professor_id:
                new_subject.laboratory_professor = await id_to_professor(
                    self.session, subject_data.laboratory_professor_id
                )
            if subject_data.seminar_professor_id:
                new_subject.seminar_professor = await id_to_professor(
                    self.session, subject_data.seminar_professor_id
                )
            if subject_data.project_professor_id:
                new_subject.project_professor = await id_to_professor(
                    self.session, subject_data.project_professor_id
                )
            self.session.add(new_subject)
            await self.session.commit()
            await self.session.refresh(new_subject)
            return subject_to_out(new_subject)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_subject(self, id: int, new_subject_data: SubjectIn) -> SubjectOut:
        try:
            subject = await self.session.get(Subject, id)
            if subject:
                subject.name = new_subject_data.name
                subject.abbreviation = new_subject_data.abbreviation.upper()
                subject.semester = new_subject_data.semester
                subject.course_professor_id = new_subject_data.course_professor_id
                subject.laboratory_professor_id = (
                    new_subject_data.laboratory_professor_id
                )
                subject.seminar_professor_id = new_subject_data.seminar_professor_id
                subject.project_professor_id = new_subject_data.project_professor_id
                if new_subject_data.programmes:
                    subject.programmes = await ids_to_programmes(
                        self.session, new_subject_data.programmes
                    )
                    subject.faculties_ids = list(
                        set(programme.faculty_id for programme in subject.programmes)
                    )
                else:
                    subject.programmes = []
                    subject.faculties_ids = []
                if new_subject_data.sessions:
                    subject.sessions = await ids_to_sessions(
                        self.session, new_subject_data.sessions
                    )
                else:
                    subject.sessions = []
                if new_subject_data.course_professor_id:
                    subject.course_professor = await id_to_professor(
                        self.session, new_subject_data.course_professor_id
                    )
                if new_subject_data.laboratory_professor_id:
                    subject.laboratory_professor = await id_to_professor(
                        self.session, new_subject_data.laboratory_professor_id
                    )
                if new_subject_data.seminar_professor_id:
                    subject.seminar_professor = await id_to_professor(
                        self.session, new_subject_data.seminar_professor_id
                    )
                if new_subject_data.project_professor_id:
                    subject.project_professor = await id_to_professor(
                        self.session, new_subject_data.project_professor_id
                    )
                await self.session.commit()
                return subject_to_out(subject)
            raise HTTPException(status_code=404, detail=f"No subject with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_subject(self, id: int):
        try:
            subject = await self.session.get(Subject, id)
            if subject:
                await self.session.delete(subject)
                await self.session.commit()
                return JSONResponse(f"Subject with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No subject with id={id}.")
        except Exception as e:
            raise e
