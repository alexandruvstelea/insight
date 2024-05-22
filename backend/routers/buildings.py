from databse import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.building import Building, BuildingInput, BuildingOutput
from sqlalchemy.orm import joinedload
from models.faculty import Faculty

router = APIRouter(prefix="/api/buildings")


@router.get("/")
def get_buildings(session: Session = Depends(get_session)) -> list:
    query = select(Building).options(joinedload(Building.faculties))
    return session.exec(query).unique()


@router.get("/{id}", response_model=BuildingOutput)
def get_buildings_by_id(id: int, session: Session = Depends(get_session)) -> Building:
    building = session.get(Building, id)
    if building:
        return building
    else:
        raise HTTPException(status_code=404, detail=f"No building with id={id}")


@router.post("/", response_model=BuildingOutput)
def add_building(
    building_input: BuildingInput, session: Session = Depends(get_session)
) -> BuildingOutput:
    new_building = Building(name=building_input.name)
    if building_input.faculties:
        faculties = session.exec(
            select(Faculty).where(Faculty.id.in_(building_input.faculties))
        ).all()
        if len(faculties) != len(building_input.faculties):
            raise HTTPException(
                status_code=404,
                detail=f"One or more faculties not found for IDs {building_input.faculties}",
            )
        for faculty in faculties:
            new_building.faculties.append(faculty)
    session.add(new_building)
    session.commit()
    session.refresh(new_building)
    return BuildingOutput.model_validate(new_building)


@router.put("/{id}", response_model=BuildingOutput)
def update_building(
    id: int, new_building: BuildingInput, session: Session = Depends(get_session)
) -> BuildingOutput:
    building = session.get(Building, id)
    if building:
        building.name = new_building.name
        session.commit()
        return BuildingOutput.model_validate(building)
    else:
        raise HTTPException(status_code=404, detail=f"No building with id={id}")


@router.delete("/{id}", status_code=204)
def delete_building(id: int, session: Session = Depends(get_session)) -> None:
    building = session.get(Building, id)
    if building:
        session.delete(building)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No building with id={id}")
