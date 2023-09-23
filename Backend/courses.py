import sqlalchemy as db
from database import Base
from sqlalchemy.types import Time
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class Course(Base):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    type = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))
    day = db.Column(db.Integer)
    week_type = db.Column(db.Integer)
    start_end = db.Column(ARRAY(Time))

    def __init__(
        self,
        subject_id: int,
        type: int,
        room_id: int,
        day: int,
        week_type: int,
        start_end: list,
    ):
        self.subject_id = subject_id
        self.type = type
        self.room_id = room_id
        self.day = day
        self.week_type = week_type
        start_end[0] = datetime.strptime(start_end[0], "%H:%M")
        start_end[1] = datetime.strptime(start_end[1], "%H:%M")
        self.start_end = start_end

    def get_subject_id(self):
        return self.subject_id

    def get_type(self):
        return self.type

    def get_room_id(self):
        return self.room_id

    def get_day(self):
        return self.day

    def get_week_type(self):
        return self.week_type

    def get_start_end(self):
        return self.start_end

    def set_subject_id(self, new_subject_id: int):
        pass

    def set_type(self, new_type: int):
        self.type = new_type

    def set_room_id(self, new_room_id: int):
        pass

    def set_day(self, new_day):
        self.day = new_day

    def set_week_type(self, new_week_type: int):
        self.week_type = new_week_type

    def set_start_end(self, new_start_end: list):
        self.start_end = new_start_end

    def __str__(self):
        return f"ID {self.id}->Subject_ID: {self.subject_id} Type: {self.type} Room_ID: {self.room_id} Day: {self.day} Week_Type: {self.week_type} Start: {self.start_end[0]} End: {self.start_end[1]}"
