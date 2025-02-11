from app.repositories.interfaces.i_subject_repository import ISubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
from app.models.subject import Subject
from app.models.programme import Programme
from app.models.session import Session
from app.schemas.subject import SubjectFilter
from typing import Optional
from app.core.logging import logger


class SubjectRepository(ISubjectRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, subject: Subject) -> Optional[Subject]:
        new_subject = Subject(
            name=subject.name,
            abbreviation=subject.abbreviation.upper(),
            semester=subject.semester,
            course_professor_id=subject.course_professor_id,
            laboratory_professor_id=subject.laboratory_professor_id,
            seminar_professor_id=subject.seminar_professor_id,
            project_professor_id=subject.project_professor_id,
            programmes=subject.programmes,
        )

        self.session.add(new_subject)
        await self.session.commit()
        await self.session.refresh(new_subject)

        return new_subject

    async def get_all(
        self, filters: Optional[SubjectFilter]
    ) -> Optional[list[Subject]]:
        conditions = []

        if filters.name:
            conditions.append(Subject.name == filters.name)
        if filters.abbreviation:
            conditions.append(Subject.abbreviation == filters.abbreviation)
        if filters.semester:
            conditions.append(Subject.semester == filters.semester)
        if filters.course_professor_id:
            conditions.append(
                Subject.course_professor_id == filters.course_professor_id
            )
        if filters.laboratory_professor_id:
            conditions.append(
                Subject.laboratory_professor_id == filters.laboratory_professor_id
            )
        if filters.seminar_professor_id:
            conditions.append(
                Subject.seminar_professor_id == filters.seminar_professor_id
            )
        if filters.project_professor_id:
            conditions.append(
                Subject.project_professor_id == filters.project_professor_id
            )
        if filters.programme_id:
            conditions.append(
                Subject.programmes.any(Programme.id == filters.programme_id)
            )
        if filters.session_id:
            conditions.append(Subject.sessions.any(Session.id == filters.session_id))

        query = select(Subject).options(joinedload(Subject.programmes))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        subjects = result.scalars().all()

        return subjects if subjects else None

    async def get_by_id(self, id: int) -> Optional[Subject]:
        subject = await self.session.get(Subject, id)
        return subject if subject else None

    async def update(self, id: int, new_subject: Subject) -> Optional[Subject]:
        subject = await self.session.get(Subject, id)

        if not subject:
            return None

        subject.name = new_subject.name
        subject.abbreviation = new_subject.abbreviation.upper()
        subject.semester = new_subject.semester
        subject.course_professor_id = new_subject.course_professor_id
        subject.laboratory_professor_id = new_subject.laboratory_professor_id
        subject.seminar_professor_id = new_subject.seminar_professor_id
        subject.project_professor_id = new_subject.project_professor_id
        subject.programmes = new_subject.programmes

        await self.session.commit()

        return subject

    async def delete(self, id: int) -> bool:
        subject = await self.session.get(Subject, id)

        if not subject:
            return False

        await self.session.delete(subject)
        await self.session.commit()

        return True
