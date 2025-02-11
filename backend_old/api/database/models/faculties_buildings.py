from sqlalchemy import Table, Column, Integer, ForeignKey
from ..main import AlchemyAsyncBase

faculties_buildings = Table(
    "faculties_buildings",
    AlchemyAsyncBase.metadata,
    Column("faculty_id", Integer, ForeignKey("faculties.id"), primary_key=True),
    Column("building_id", Integer, ForeignKey("buildings.id"), primary_key=True),
)
