from sqlmodel import SQLModel, Field


class FacultyBuildingLink(SQLModel, table=True):
    __tablename__: str = "faculties_buildings"
    faculty_id: int = Field(default=None, foreign_key="faculties.id", primary_key=True)
    building_id: int = Field(default=None, foreign_key="buildings.id", primary_key=True)
