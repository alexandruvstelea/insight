import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Programme(Base):
    __tablename__ = "Programmes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    abbreviation = db.Column(db.Text)

    def __init__(self, name: str, abbreviation: str):
        self.name = name
        self.abbreviation = abbreviation

    def get_name(self):
        return self.name

    def get_abbreviation(self):
        return self.abbreviation

    def set_name(self, new_name: str):
        self.name = new_name

    def set_abbreviation(self, new_abbreviation: str):
        self.abbreviation = new_abbreviation

    def __str__(self):
        return f"ID: {self.id}->Name: {self.name} Abbreviation: {self.abbreviation}"
