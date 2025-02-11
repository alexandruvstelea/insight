from app.repositories.interfaces.i_faculty_repository import IFacultyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
from app.models.faculty import Faculty
from app.models.building import Building
from app.models.programme import Programme
from app.models.professor import Professor
from typing import Optional
from app.schemas.faculty import FacultyFilter
from app.core.logging import logger


class FacultyRepository(IFacultyRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, faculty: Faculty) -> Optional[Faculty]:
        new_faculty = Faculty(
            name=faculty.name,
            abbreviation=faculty.abbreviation.upper(),
            buildings=faculty.buildings,
            professors=faculty.professors,
            programmes=faculty.programmes,
        )

        self.session.add(new_faculty)
        await self.session.commit()
        await self.session.refresh(new_faculty)

        return new_faculty

    async def get_all(
        self, filters: Optional[FacultyFilter]
    ) -> Optional[list[Faculty]]:
        conditions = []

        if filters.name:
            conditions.append(Faculty.name == filters.name)
        if filters.abbreviation:
            conditions.append(Faculty.abbreviation == filters.abbreviation)
        if filters.building_id:
            conditions.append(Faculty.buildings.any(Building.id == filters.building_id))
        if filters.professor_id:
            conditions.append(
                Faculty.professors.any(Professor.id == filters.professor_id)
            )
        if filters.progamme_id:
            conditions.append(
                Faculty.programmes.any(Programme.id == filters.progamme_id)
            )

        query = select(Faculty).options(joinedload(Faculty.buildings))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        faculties = result.scalars().all()

        return faculties if faculties else None

    async def get_by_id(self, id: int) -> Optional[Faculty]:
        faculty = await self.session.get(Faculty, id)
        return faculty if faculty else None

    async def update(self, id: int, new_faculty: Faculty) -> Optional[Faculty]:
        faculty = await self.session.get(Faculty, id)

        if not faculty:
            return None

        faculty.name = new_faculty.name
        faculty.abbreviation = new_faculty.abbreviation.upper()
        faculty.buildings = new_faculty.buildings
        faculty.professors = new_faculty.professors
        faculty.programmes = new_faculty.programmes

        await self.session.commit()

        return faculty

    async def delete(self, id: int) -> bool:
        faculty = await self.session.get(Faculty, id)

        if not faculty:
            return False

        await self.session.delete(faculty)
        await self.session.commit()

        return True
