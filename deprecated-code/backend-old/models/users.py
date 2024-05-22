from __init__ import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    programme_id = db.Column(db.Integer, db.ForeignKey("Programmes.id"))
    user_type = db.Column(db.Integer)
    registration_code = db.Column(db.Integer)
    active = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self,
        email: str,
        password: str,
        programme_id: int,
        registration_code: int,
    ):
        self.email = email
        self.password = password
        self.programme_id = programme_id
        self.user_type = 1
        self.registration_code = registration_code
        self.active = 0
