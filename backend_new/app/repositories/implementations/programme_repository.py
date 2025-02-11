from app.repositories.interfaces.i_programme_repository import IProgrammeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
from app.models.programme import Programme
from app.models.subject import Subject
from app.schemas.programme import ProgrammeFilter
from typing import Optional
from app.core.logging import logger


class ProgrammeRepository(IProgrammeRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, programme: Programme) -> Optional[Programme]:
        new_programme = Programme(
            name=programme.name,
            abbreviation=programme.abbreviation.upper(),
            type=programme.type,
            faculty_id=programme.faculty_id,
            faculty=programme.faculty,
            subjects=programme.subjects,
        )

        self.session.add(new_programme)
        await self.session.commit()
        await self.session.refresh(new_programme)

        return new_programme

    async def get_all(
        self, filters: Optional[ProgrammeFilter]
    ) -> Optional[list[Programme]]:
        conditions = []

        if filters.name:
            conditions.append(Programme.name == filters.name)
        if filters.abbreviation:
            conditions.append(Programme.abbreviation == filters.abbreviation)
        if filters.type:
            conditions.append(Programme.type == filters.type)
        if filters.faculty_id:
            conditions.append(Programme.faculty == filters.faculty_id)
        if filters.subject_id:
            conditions.append(Programme.subjects.any(Subject.id == filters.subject_id))

        query = select(Programme).options(joinedload(Programme.subjects))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        programmes = result.scalars().all()

        return programmes if programmes else None

    async def get_by_id(self, id: int) -> Optional[Programme]:
        programme = await self.session.get(Programme, id)
        return programme if programme else None

    async def update(self, id: int, new_programme: Programme) -> Optional[Programme]:
        programme = await self.session.get(Programme, id)

        if not programme:
            return None

        programme.name = new_programme.name
        programme.abbreviation = new_programme.abbreviation.upper()
        programme.type = new_programme.type
        programme.faculty_id = new_programme.faculty_id
        programme.faculty = new_programme.faculty
        programme.subjects = new_programme.subjects

        await self.session.commit()

        return programme

    async def delete(self, id: int) -> bool:
        programme = await self.session.get(Programme, id)

        if not programme:
            return False

        await self.session.delete(programme)
        await self.session.commit()

        return True
