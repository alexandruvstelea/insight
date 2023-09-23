import sqlalchemy as db
from database import Base


class Room(Base):
    __tablename__ = "Rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, new_name: str):
        self.name = new_name

    def __str__(self):
        return f"ID:{self.id}->Room name: {self.name}"
