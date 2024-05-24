from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import FacultyIn, FacultyOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import FacultyOperations
from http import HTTPStatus
from typing import List

faculties_router = APIRouter(prefix="/api/faculties")


@faculties_router.get("/", response_model=List[FacultyOut], status_code=HTTPStatus.OK)
async def get_faculties(
    session: AsyncSession = Depends(get_session),
) -> List[FacultyOut]:
    response = await FacultyOperations(session).get_faculties()
    return response


@faculties_router.get("/{id}", response_model=FacultyOut, status_code=HTTPStatus.OK)
async def get_faculties_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> FacultyOut:
    response = await FacultyOperations(session).get_faculty_by_id(id)
    return response


@faculties_router.post("/", response_model=FacultyOut, status_code=HTTPStatus.CREATED)
async def add_faculty(
    faculty_data: FacultyIn, session: AsyncSession = Depends(get_session)
) -> FacultyOut:
    response = await FacultyOperations(session).add_faculty(faculty_data)
    return response


@faculties_router.put("/{id}", response_model=FacultyOut, status_code=HTTPStatus.OK)
async def update_faculty(
    id: int, new_faculty_data: FacultyIn, session: AsyncSession = Depends(get_session)
) -> FacultyOut:
    response = await FacultyOperations(session).update_faculty(id, new_faculty_data)
    return response


@faculties_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_faculty(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await FacultyOperations(session).delete_faculty(id)
    return response
