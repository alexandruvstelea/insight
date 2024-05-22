from __init__ import db


class Room(db.Model):
    __tablename__ = "Rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"ID:{self.id}->Room name: {self.name}"
