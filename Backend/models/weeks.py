from __init__ import db


class Week(db.Model):
    __tablename__ = "Weeks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    semester = db.Column(db.Integer)

    def __init__(
        self,
        start: str,
        end: str,
        semester: int,
    ):
        self.start = start
        self.end = end
        self.semester = semester
