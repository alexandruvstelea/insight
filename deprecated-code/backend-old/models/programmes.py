from __init__ import db


class Programme(db.Model):
    __tablename__ = "Programmes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    abbreviation = db.Column(db.Text)

    def __init__(self, name: str, abbreviation: str):
        self.name = name
        self.abbreviation = abbreviation
