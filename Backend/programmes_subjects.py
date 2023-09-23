import sqlalchemy as db
from database import Base


class ProgrammesSubjects(Base):
    __tablename__ = "Programmes_Subjects"

    programme_id = db.Column(
        db.Integer, db.ForeignKey("Programmes.id"), primary_key=True
    )
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"), primary_key=True)

    def __init__(self, programme_id: int, subject_id: int):
        self.programme_id = programme_id
        self.subject_id = subject_id

    def __str__(self):
        return f"Programme_ID: {self.programme_id} Subject_ID: {self.subject_id}"
