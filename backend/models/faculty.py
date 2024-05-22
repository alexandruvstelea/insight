from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .faculties_buildings import FacultyBuildingLink
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .building import BuildingOutput, Building


class FacultyBase(SQLModel):
    name: str
    abbreviation: str


class Faculty(FacultyBase, table=True):
    __tablename__: str = "faculties"
    id: Optional[int] = Field(default=None, primary_key=True)
    buildings: List["Building"] = Relationship(
        link_model=FacultyBuildingLink, back_populates="faculties"
    )


class FacultyInput(FacultyBase):
    buildings: Optional[List[int]] = Field(default_factory=list)


class FacultyOutput(FacultyBase):
    id: int
    buildings: List["BuildingOutput"] = Field(default_factory=list)
