from __init__ import db


class Comment(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    is_anonymous = db.Column(db.Boolean)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subjects.id"))
    datetime = db.Column(db.DateTime(timezone=False))

    def __init__(
        self,
        comment: str,
        is_anonymous: bool,
        subject_id: int,
        datetime,
    ):
        self.comment = comment
        self.is_anonymous = is_anonymous
        self.subject_id = subject_id
        self.datetime = datetime
