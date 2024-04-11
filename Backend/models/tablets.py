from __init__ import db


class Tablet(db.Model):
    __tablename__ = "Tablets"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))
    last_ping = db.Column(db.DateTime(timezone=False))

    def __init__(self, room_id: int, last_ping):
        self.room_id = room_id
        self.last_ping = last_ping
