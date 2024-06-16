from sqlalchemy import Table, Column, Integer, ForeignKey
from ..main import AlchemyAsyncBase

programmes_subjects = Table(
    "programmes_subjects",
    AlchemyAsyncBase.metadata,
    Column("programme_id", Integer, ForeignKey("programmes.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)
