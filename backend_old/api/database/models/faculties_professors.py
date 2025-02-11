from sqlalchemy import Table, Column, Integer, ForeignKey
from ..main import AlchemyAsyncBase

faculties_professors = Table(
    "faculties_professors",
    AlchemyAsyncBase.metadata,
    Column("faculty_id", Integer, ForeignKey("faculties.id"), primary_key=True),
    Column("professor_id", Integer, ForeignKey("professors.id"), primary_key=True),
)
