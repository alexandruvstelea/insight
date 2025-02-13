from app.repositories.interfaces.i_professor_repository import IProfessorRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.models.professor import Professor
from app.models.faculty import Faculty
from app.models.subject import Subject
from app.schemas.professor import ProfessorFilter
from typing import Optional
from app.core.logging import logger


class ProfessorRepository(IProfessorRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, professor: Professor) -> Optional[Professor]:
        try:
            self.session.add(professor)
            await self.session.commit()
            await self.session.refresh(professor)
            return professor
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self, filters: Optional[ProfessorFilter]
    ) -> Optional[list[Professor]]:
        try:
            query = select(Professor).options(joinedload(Professor.faculties))

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            professors = result.scalars().all()

            return professors if professors else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Professor]:
        try:
            professor = await self.session.get(Professor, id)
            return professor if professor else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_professor: Professor) -> Optional[Professor]:
        try:
            professor = await self.session.get(Professor, id)

            if not professor:
                return None

            professor.first_name = new_professor.first_name
            professor.last_name = new_professor.last_name
            professor.gender = new_professor.gender
            professor.faculties = new_professor.faculties
            professor.courses = new_professor.courses
            professor.laboratories = new_professor.laboratories
            professor.seminars = new_professor.seminars
            professor.projects = new_professor.projects

            await self.session.commit()

            return professor
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            professor = await self.session.get(Professor, id)

            if not professor:
                return False

            await self.session.delete(professor)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[ProfessorFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Professor)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def __get_conditions(filters: ProfessorFilter) -> Optional[list]:
        conditions = []

        if filters.first_name:
            conditions.append(Professor.first_name == filters.first_name)
        if filters.last_name:
            conditions.append(Professor.last_name == filters.last_name)
        if filters.gender:
            conditions.append(Professor.gender == filters.gender)
        if filters.faculty_id:
            conditions.append(Professor.faculties.any(Faculty.id == filters.faculty_id))
        if filters.course_id:
            conditions.append(
                Professor.courses.any(
                    and_(
                        Subject.id == filters.course_id,
                        Subject.course_professor_id == Professor.id,
                    )
                )
            )
        if filters.laboratory_id:
            conditions.append(
                Professor.courses.any(
                    and_(
                        Subject.id == filters.course_id,
                        Subject.laboratory_professor_id == Professor.id,
                    )
                )
            )
        if filters.seminar_id:
            conditions.append(
                Professor.courses.any(
                    and_(
                        Subject.id == filters.course_id,
                        Subject.seminar_professor_id == Professor.id,
                    )
                )
            )
        if filters.project_id:
            conditions.append(
                Professor.courses.any(
                    and_(
                        Subject.id == filters.course_id,
                        Subject.project_professor_id == Professor.id,
                    )
                )
            )

        return conditions if conditions else None

        # new_professor = Professor(
        #     first_name=professor.first_name,
        #     last_name=professor.last_name,
        #     gender=professor.gender,
        #     faculties=professor.faculties,
        #     courses=professor.courses,
        #     laboratories=professor.laboratories,
        #     seminars=professor.seminars,
        #     projects=professor.projects,
        # )
