from flask import Blueprint, jsonify, request
from models.professors import Professor
from __init__ import db
from sqlalchemy import exc

professor_bp = Blueprint("professors", __name__)


@professor_bp.route("/professors", methods=["POST"])
def create_professor():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    title = request.form["title"]
    new_professor = Professor(first_name, last_name, title)
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
                "first_name": professor.first_name,
                "last_name": professor.last_name,
                "title": professor.title,
            }
        )
    return jsonify(professors_list)


@professor_bp.route("/professors/<int:professor_id>", methods=["GET"])
def get_professor_by_id(professor_id):
    professor = db.session.query(Professor).filter_by(id=professor_id).first()
    if professor:
        return {
            "id": professor.id,
            "first_name": professor.first_name,
            "last_name": professor.last_name,
            "title": professor.title,
        }
    else:
        return {"response": f"No professor with ID={professor_id} found."}


@professor_bp.route("/professors/<int:professor_id>", methods=["PUT"])
def update_professor(professor_id):
    new_first_name = request.form["new_first_name"]
    new_last_name = request.form["new_last_name"]
    new_title = request.form["new_title"]
    try:
        affected_rows = (
            db.session.query(Professor)
            .filter_by(id=professor_id)
            .update(
                {
                    "first_name": new_first_name,
                    "last_name": new_last_name,
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
