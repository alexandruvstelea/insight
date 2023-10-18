from __init__ import db


class Subject(db.Model):
    __tablename__ = "Subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    abbreviation = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey("Professors.id"))
    semester = db.Column(db.Integer)

    def __init__(self, name: str, abbreviation: str, professor_id: int, semester: int):
        self.name = name
        self.abbreviation = abbreviation
        self.professor_id = professor_id
        self.semester = semester

    def __str__(self):
        return f"ID: {self.id}->Name: {self.name} Abbreviation: {self.abbreviation} Professor_ID: {self.professor_id} Semester: {self.semester}"
