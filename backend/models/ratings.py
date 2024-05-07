from __init__ import db


class Rating(db.Model):
    __tablename__ = "Ratings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_clarity = db.Column(db.Integer)
    rating_interactivity = db.Column(db.Integer)
    rating_relevance = db.Column(db.Integer)
    rating_comprehension = db.Column(db.Integer)
    rating_overall = db.Column(db.Float)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    datetime = db.Column(db.DateTime(timezone=False))

    def __init__(
        self,
        rating_clarity: int,
        rating_interactivity: int,
        rating_relevance: int,
        rating_comprehension: int,
        rating_overall: int,
        subject_id: int,
        datetime,
    ):
        self.rating_clarity = rating_clarity
        self.rating_interactivity = rating_interactivity
        self.rating_relevance = rating_relevance
        self.rating_comprehension = rating_comprehension
        self.rating_overall = rating_overall
        self.subject_id = subject_id
        self.datetime = datetime

    def __str__(self):
        return f"ID={self.id}->Rating={self.rating}, Subject_ID={self.subject_id},Timestamp={self.datetime}"
