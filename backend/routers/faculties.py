from databse import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.faculty import FacultyInput, FacultyOutput, Faculty
from models.building import BuildingOutput

router = APIRouter(prefix="/api/faculties")


@router.get("/")
def get_faculties(session: Session = Depends(get_session)) -> list:
    query = select(Faculty)
    return session.exec(query).all()


@router.get("/{id}", response_model=FacultyOutput)
def get_faculties_by_id(id: int, session: Session = Depends(get_session)) -> Faculty:
    faculty = session.get(Faculty, id)
    if faculty:
        return faculty
    else:
        raise HTTPException(status_code=404, detail=f"No faculty with id={id}")


@router.post("/", response_model=FacultyInput)
def add_faculty(
    faculty_input: FacultyInput, session: Session = Depends(get_session)
) -> Faculty:
    new_faculty = Faculty.model_validate(faculty_input)
    session.add(new_faculty)
    session.commit()
    session.refresh(new_faculty)
    return new_faculty


@router.put("/{id}", response_model=Faculty)
def update_faculty(
    id: int, new_faculty: FacultyInput, session: Session = Depends(get_session)
) -> Faculty:
    faculty = session.get(Faculty, id)
    if faculty:
        faculty.name = new_faculty.name
        faculty.abbreviation = new_faculty.abbreviation
        session.commit()
        return faculty
    else:
        raise HTTPException(status_code=404, detail=f"No faculty with id={id}")


@router.delete("/{id}", status_code=204)
def delete_faculty(id: int, session: Session = Depends(get_session)) -> None:
    faculty = session.get(Faculty, id)
    if faculty:
        session.delete(faculty)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No faculty with id={id}")
