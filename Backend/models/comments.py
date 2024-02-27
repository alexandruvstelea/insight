from __init__ import db


class Comment(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    code = db.Column(db.String)
    comment = db.Column(db.String)
    is_like = db.Column(db.Integer)
    is_anonymous = db.Column(db.Boolean)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    grade = db.Column(db.Integer)
    datetime = db.Column(db.DateTime(timezone=False))

    def __init__(
        self,
        email: str,
        comment: str,
        is_like: int,
        is_anonymous: bool,
        subject_id: int,
        grade: int,
        datetime,
    ):
        self.email = email
        self.comment = comment
        self.is_like = is_like
        self.is_anonymous = is_anonymous
        self.subject_id = subject_id
        self.grade = grade
        self.datetime = datetime
