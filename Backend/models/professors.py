from __init__ import db


class Professor(db.Model):
    __tablename__ = "Professors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    title = db.Column(db.Text)

    def __init__(self, name: str, surname: str, title: str):
        self.name = name
        self.surname = surname
        self.title = title

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_title(self):
        return self.title

    def set_name(self, new_name: str):
        self.name = new_name

    def set_surname(self, new_surname: str):
        self.surname = new_surname

    def set_title(self, new_title: str):
        self.title = new_title

    def __str__(self):
        return f"ID: {self.id}->Surname: {self.surname.upper()} Name: {self.name.upper()} Title: {self.title.upper()}"
