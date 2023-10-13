from flask import Blueprint, jsonify, request
from models.professors import Professor
from __init__ import db
from sqlalchemy import exc

professor_bp = Blueprint("professors", __name__)


@professor_bp.route("/professors", methods=["POST"])
def create_professor():
    name = request.form["name"]
    surname = request.form["surname"]
    title = request.form["title"]
    new_professor = Professor(name, surname, title)
    try:
        db.session.add(new_professor)
        db.session.commit()
        return {"response": "New professor added to database"}
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@professor_bp.route("/professors", methods=["GET"])
def get_professors():
    professors = db.session.query(Professor).all()
    professors_list = []
    for professor in professors:
        professors_list.append(
            {
                "id": professor.id,
                "name": professor.name,
                "surname": professor.surname,
                "title": professor.title,
            }
        )
    return jsonify(professors_list)


@professor_bp.route("/professors/<int:professor_id>", methods=["PUT"])
def update_professor(professor_id):
    new_name = request.form["new_name"]
    new_surname = request.form["new_surname"]
    new_title = request.form["new_title"]
    try:
        affected_rows = (
            db.session.query(Professor)
            .filter_by(id=professor_id)
            .update(
                {
                    "name": new_name,
                    "surname": new_surname,
                    "title": new_title,
                }
            )
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Professor with ID={professor_id} updated"}
    else:
        return {"response": f"No professor with ID={professor_id} to update"}


@professor_bp.route("/professors/<int:professor_id>", methods=["DELETE"])
def delete_professor(professor_id):
    affected_rows = db.session.query(Professor).filter_by(id=professor_id).delete()
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Professor with ID={professor_id} deleted"}
    else:
        return {"response": f"No professor with ID={professor_id} to delete"}
