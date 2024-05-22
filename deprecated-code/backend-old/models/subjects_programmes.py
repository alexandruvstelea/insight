from __init__ import db

subjects_programmes = db.Table(
    "Subjects_Programmes",
    db.Column("subject_id", db.Integer, db.ForeignKey("Subjects.id"), primary_key=True),
    db.Column(
        "programme_id", db.Integer, db.ForeignKey("Programmes.id"), primary_key=True
    ),
)
