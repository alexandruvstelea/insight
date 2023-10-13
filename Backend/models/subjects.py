from __init__ import db


class Subject(db.Model):
    __tablename__ = "Subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    abbreviation = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey("Professors.id"))

    def __init__(self, name: str, abbreviation: str, professor_id: int):
        self.name = name
        self.abbreviation = abbreviation
        self.professor_id = professor_id

    def get_name(self):
        return self.name

    def get_abbreviation(self):
        return self.abbreviation

    def get_professor_id(self):
        return self.professor_id

    def set_name(self, new_name: str):
        self.name = new_name

    def set_abbreviation(self, new_abbreviation: str):
        self.abbreviation = new_abbreviation

    def set_professor_id(self, new_professor_id: int):
        pass
        # TBD

    def __str__(self):
        return f"ID: {self.id}->Name: {self.name} Abbreviation: {self.abbreviation} Professor_ID: {self.professor_id}"
