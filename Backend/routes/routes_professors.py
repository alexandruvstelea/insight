from flask import Blueprint, jsonify, request, abort
from models.professors import Professor
from __init__ import db
from sqlalchemy import exc
from bleach import clean

professor_bp = Blueprint("professors", __name__)


@professor_bp.route("/professors", methods=["POST"])
def create_professor():
    try:
        first_name = clean(request.form["first_name"])
        last_name = clean(request.form["last_name"])
        title = clean(request.form["title"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    new_professor = Professor(first_name, last_name, title)
    try:
        with db.session.begin():
            db.session.add(new_professor)
            db.session.commit()
            return {"response": "New professor added to database"}, 200
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while adding object to database.\n {str(e)}")


@professor_bp.route("/professors", methods=["GET"])
def get_professors():
    try:
        professors = db.session.query(Professor).all()
        professors_list = []
        if professors:
            for professor in professors:
                professors_list.append(
                    {
                        "id": professor.id,
                        "first_name": professor.first_name,
                        "last_name": professor.last_name,
                        "title": professor.title,
                    }
                )
            return jsonify(professors_list), 200
        else:
            abort(404, "No professors found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")


@professor_bp.route("/professors/<int:professor_id>", methods=["GET"])
def get_professor_by_id(professor_id):
    try:
        professor = db.session.query(Professor).filter_by(id=professor_id).first()
        if professor:
            return {
                "id": professor.id,
                "first_name": professor.first_name,
                "last_name": professor.last_name,
                "title": professor.title,
            }, 200
        else:
            return abort(404, f"No professor with ID={professor_id} found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")


@professor_bp.route("/professors/<int:professor_id>", methods=["PUT"])
def update_professor(professor_id):
    try:
        new_first_name = clean(request.form["new_first_name"])
        new_last_name = clean(request.form["new_last_name"])
        new_title = clean(request.form["new_title"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    try:
        with db.session.begin():
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
            if affected_rows > 0:
                db.session.commit()
                return {"response": f"Professor with ID={professor_id} updated"}, 200
            else:
                return abort(404, f"No professor with ID={professor_id} to update")
    except exc.SQLAlchemyError as e:
        return abort(500, f"An error while updating the object. {str(e)}")


@professor_bp.route("/professors/<int:professor_id>", methods=["DELETE"])
def delete_professor(professor_id):
    try:
        with db.session.begin():
            affected_rows = (
                db.session.query(Professor).filter_by(id=professor_id).delete()
            )
            if affected_rows > 0:
                db.session.commit()
                return {"response": f"Professor with ID={professor_id} deleted"}, 200
            else:
                return abort(404, f"No professor with ID={professor_id} to delete")
    except exc.SQLAlchemyError as e:
        return abort(500, f"An error while updating the object. {str(e)}")
