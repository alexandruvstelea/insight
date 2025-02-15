from app.repositories.interfaces.i_subject_repository import ISubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
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
        try:
            self.session.add(subject)
            await self.session.commit()
            await self.session.refresh(subject)
            return subject
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self, filters: Optional[SubjectFilter]
    ) -> Optional[list[Subject]]:
        try:
            query = select(Subject).options(joinedload(Subject.programmes))

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            subjects = result.scalars().all()

            return subjects if subjects else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Subject]:
        try:
            subject = await self.session.get(Subject, id)
            return subject if subject else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_subject: Subject) -> Optional[Subject]:
        try:
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
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            subject = await self.session.get(Subject, id)

            if not subject:
                return False

            await self.session.delete(subject)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[SubjectFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Subject)

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def _get_conditions(self, filters: SubjectFilter) -> Optional[list]:
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

        return conditions if conditions else None
        # new_subject = Subject(
        #     name=subject.name,
        #     abbreviation=subject.abbreviation.upper(),
        #     semester=subject.semester,
        #     course_professor_id=subject.course_professor_id,
        #     laboratory_professor_id=subject.laboratory_professor_id,
        #     seminar_professor_id=subject.seminar_professor_id,
        #     project_professor_id=subject.project_professor_id,
        #     programmes=subject.programmes,
        # )
