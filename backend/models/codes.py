from __init__ import db


class Code(db.Model):
    __tablename__ = "Codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))

    def __init__(
        self,
        code: int,
        room_id: int,
    ):
        self.code = code
        self.room_id = room_id
