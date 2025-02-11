from app.repositories.interfaces.i_professor_repository import IProfessorRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
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
        new_professor = Professor(
            first_name=professor.first_name,
            last_name=professor.last_name,
            gender=professor.gender,
            faculties=professor.faculties,
            courses=professor.courses,
            laboratories=professor.laboratories,
            seminars=professor.seminars,
            projects=professor.projects,
        )

        self.session.add(new_professor)
        await self.session.commit()
        await self.session.refresh(new_professor)

        return new_professor

    async def get_all(
        self, filters: Optional[ProfessorFilter]
    ) -> Optional[list[Professor]]:
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

        query = select(Professor).options(joinedload(Professor.faculties))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        professors = result.scalars().all()

        return professors if professors else None

    async def get_by_id(self, id: int) -> Optional[Professor]:
        professor = await self.session.get(Professor, id)
        return professor if professor else None

    async def update(self, id: int, new_professor: Professor) -> Optional[Professor]:
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

    async def delete(self, id: int) -> bool:
        professor = await self.session.get(Professor, id)

        if not professor:
            return False

        await self.session.delete(professor)
        await self.session.commit()

        return True
