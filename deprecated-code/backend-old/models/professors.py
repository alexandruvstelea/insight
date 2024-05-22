from __init__ import db


class Professor(db.Model):
    __tablename__ = "Professors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    gender = db.Column(db.Text)

    def __init__(self, first_name: str, last_name: str, gender: str):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

    def __str__(self):
        return f"ID: {self.id}->First Name={self.first_name.upper()}, Last Name={self.last_name.upper()}, Gender={self.gender}"
