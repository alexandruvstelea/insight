from sqlalchemy import select
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
from ..programmes.utils import programme_to_minimal


class SubjectOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_subjects(self) -> List[SubjectOut]:
        try:
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
                abbreviation=subject_data.abbreviation,
                semester=subject_data.semester,
                course_professor_id=subject_data.course_professor_id,
                laboratory_professor_id=subject_data.laboratory_professor_id,
                seminar_professor_id=subject_data.seminar_professor_id,
                project_professor_id=subject_data.project_professor_id,
            )
            if subject_data.programmes:
                new_subject.programmes = [
                    programme_to_minimal(programme)
                    for programme in subject_data.programmes
                ]
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

    async def update_room(self, id: int, new_room_data: SubjectIn) -> SubjectOut:
        try:
            room = await self.session.get(Room, id)
            if room:
                room.name = new_room_data.name
                if new_room_data.building_id:
                    room.building_id = new_room_data.building_id
                    room.building = await id_to_building(
                        self.session, new_room_data.building_id
                    )
                await self.session.commit()
                return room_to_out(room)
            raise HTTPException(status_code=404, detail=f"No room with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_room(self, id: int):
        try:
            room = await self.session.get(Room, id)
            if room:
                await self.session.delete(room)
                await self.session.commit()
                return JSONResponse(f"Room with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No room with id={id}.")
        except Exception as e:
            raise e
