from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from .faculties_buildings import FacultyBuildingLink
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .faculty import Faculty, FacultyOutput


class BuildingBase(SQLModel):
    name: str


class Building(BuildingBase, table=True):
    __tablename__: str = "buildings"
    id: Optional[int] = Field(default=None, primary_key=True)
    faculties: List["Faculty"] = Relationship(
        link_model=FacultyBuildingLink, back_populates="buildings"
    )


class BuildingInput(BuildingBase):
    faculties: Optional[List[int]] = Field(default_factory=list)


class BuildingOutput(BuildingBase):
    id: int
    faculties: List["FacultyOutput"] = Field(default_factory=list)
