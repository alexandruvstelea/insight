from __init__ import db
from sqlalchemy.types import Time
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class Course(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    type = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))
    day = db.Column(db.Integer)
    week_type = db.Column(db.Integer)
    start_end = db.Column(ARRAY(Time))
    semester = db.Column(db.Integer)

    def __init__(
        self,
        subject_id: int,
        type: int,
        room_id: int,
        day: int,
        week_type: int,
        start_end: list,
        semester: int,
    ):
        self.subject_id = subject_id
        self.type = type
        self.room_id = room_id
        self.day = day
        self.week_type = week_type
        start_end[0] = datetime.strptime(start_end[0], "%H:%M")
        start_end[1] = datetime.strptime(start_end[1], "%H:%M")
        self.start_end = start_end
        self.semester = semester

    def __str__(self):
        return f"ID {self.id}->Subject_ID={self.subject_id}, Type={self.type}, Room_ID={self.room_id}, Day={self.day}, Week_Type={self.week_type}, Start={self.start_end[0]}, End={self.start_end[1]}, Semester={self.semester}"
