from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.programme import Programme
from .schemas import ProgrammeOut, ProgrammeIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from ..faculties.utils import id_to_faculty
from ..subjects.utils import ids_to_subjects
from .utils import programme_to_out


class ProgrammeOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_programmes(self) -> List[ProgrammeOut]:
        try:
            query = select(Programme).options(
                joinedload(Programme.faculty), joinedload(Programme.subjects)
            )
            result = await self.session.execute(query)
            programmes = result.scalars().unique().all()
            if programmes:
                return [
                    programme_to_out(programme)
                    for programme in sorted(list(programmes), key=lambda x: x.name)
                ]
            raise HTTPException(status_code=404, detail="No programmes found.")
        except Exception as e:
            raise e

    async def get_programme_by_id(self, id: int) -> ProgrammeOut:
        programme = await self.session.get(Programme, id)
        try:
            if programme:
                return programme_to_out(programme)
            raise HTTPException(status_code=404, detail=f"No programme with id={id}.")
        except Exception as e:
            raise e

    async def add_programme(self, programme_data: ProgrammeIn) -> ProgrammeOut:
        try:
            new_programme = Programme(
                name=programme_data.name,
                abbreviation=programme_data.abbreviation,
                type=programme_data.type,
                faculty_id=programme_data.faculty_id,
                faculty=await id_to_faculty(self.session, programme_data.faculty_id),
            )
            if programme_data.subjects:
                new_programme.subjects = await ids_to_subjects(
                    self.session, programme_data.subjects
                )
            self.session.add(new_programme)
            await self.session.commit()
            await self.session.refresh(new_programme)
            return programme_to_out(new_programme)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_programme(
        self, id: int, new_programme_data: ProgrammeIn
    ) -> ProgrammeOut:
        try:
            programme = await self.session.get(Programme, id)
            if programme:
                programme.name = new_programme_data.name
                programme.abbreviation = new_programme_data.abbreviation
                programme.type = new_programme_data.type
                programme.faculty_id = new_programme_data.faculty_id
                programme.faculty = await id_to_faculty(
                    self.session, new_programme_data.faculty_id
                )
                if new_programme_data.subjects:
                    programme.subjects = [
                        ids_to_subjects(subject)
                        for subject in new_programme_data.subjects
                    ]
                await self.session.commit()
                return programme_to_out(programme)
            raise HTTPException(status_code=404, detail=f"No programme with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_programme(self, id: int):
        try:
            programme = await self.session.get(Programme, id)
            if programme:
                await self.session.delete(programme)
                await self.session.commit()
                return JSONResponse(f"Programme with ID={id} deleted.")
            else:
                raise HTTPException(
                    status_code=404, detail=f"No programme with id={id}."
                )
        except Exception as e:
            raise e
