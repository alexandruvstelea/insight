from datetime import datetime
from __init__ import db


class SubjectLike(db.Model):
    __tablename__ = "subject_likes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    ip_address = db.Column(db.String(45))
    like_dislike = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, subject_id: int, ip_address: str, like_dislike: bool):
        self.subject_id = subject_id
        self.ip_address = ip_address
        self.like_dislike = like_dislike

    def __str__(self):
        like_or_dislike = "Like" if self.like_dislike else "Dislike"
        return f"ID: {self.id}, Subject ID: {self.subject_id}, IP: {self.ip_address}, Action: {like_or_dislike}, Created At: {self.created_at}"
