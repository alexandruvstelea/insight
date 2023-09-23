import sqlalchemy as db
from database import Base


class Rating(Base):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("Room.id"))
    datetime = db.Column(db.DateTime(timezone=False))

    def __init__(self, rating: int, subject_id: int, room_id: int, datetime):
        self.rating = rating

    def get_rating(self):
        return self.rating

    def set_rating(self, new_rating: str):
        self.rating = new_rating

    def __str__(self):
        return f"ID:{self.id}->Rating: {self.rating}"
