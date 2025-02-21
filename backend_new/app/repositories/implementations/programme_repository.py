from app.repositories.interfaces.i_programme_repository import IProgrammeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.models.programme import Programme
from app.models.subject import Subject
from app.schemas.programme import ProgrammeFilter
from typing import Optional
from app.core.logging import logger


class ProgrammeRepository(IProgrammeRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, programme: Programme) -> Optional[Programme]:
        try:
            self.session.add(programme)
            await self.session.commit()
            await self.session.refresh(programme)
            return programme
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self, filters: Optional[ProgrammeFilter]
    ) -> Optional[list[Programme]]:
        try:
            query = select(Programme).options(joinedload(Programme.subjects))

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            programmes = result.scalars().unique().all()

            return programmes if programmes else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Programme]:
        try:
            programme = await self.session.get(Programme, id)
            return programme if programme else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_programme: Programme) -> Optional[Programme]:
        try:
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
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            programme = await self.session.get(Programme, id)

            if not programme:
                return False

            await self.session.delete(programme)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[ProgrammeFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Programme)

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

    def __get_conditions(self, filters: ProgrammeFilter) -> Optional[list]:
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

        return conditions if conditions else None
