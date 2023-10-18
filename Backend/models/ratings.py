from __init__ import db


class Rating(db.Model):
    __tablename__ = "Ratings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))
    datetime = db.Column(db.DateTime(timezone=False))

    def __init__(self, rating: int, subject_id: int, room_id: int, datetime):
        self.rating = rating
        self.subject_id = subject_id
        self.room_id = room_id
        self.datetime = datetime

    def __str__(self):
        return f"ID:{self.id}->Rating: {self.rating}"
