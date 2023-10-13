from flask import Blueprint, jsonify, request
from models.programmes import Programme
from __init__ import db
from sqlalchemy import exc

programme_bp = Blueprint("programmes", __name__)


@programme_bp.route("/programmes", methods=["POST"])
def create_programme():
    name = request.form["name"]
    abbreviation = request.form["abbreviation"]
    new_programme = Programme(name, abbreviation)
    try:
        db.session.add(new_programme)
        db.session.commit()
        return {"response": "New programme added to database"}
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@programme_bp.route("/programmes", methods=["GET"])
def get_programmes():
    programmes = db.session.query(Programme).all()
    programmes_list = []
    for programme in programmes:
        programmes_list.append(
            {
                "id": programme.id,
                "name": programme.name,
                "abbreviation": programme.abbreviation,
            }
        )
    return jsonify(programmes_list)


@programme_bp.route("/programmes/<int:programme_id>", methods=["PUT"])
def update_programme(programme_id):
    new_name = request.form["new_name"]
    new_abbreviation = request.form["new_abbreviation"]
    try:
        affected_rows = (
            db.session.query(Programme)
            .filter_by(id=programme_id)
            .update(
                {
                    "name": new_name,
                    "abbreviation": new_abbreviation,
                }
            )
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Programme with ID={programme_id} updated"}
    else:
        return {"response": f"No programme with ID={programme_id} to update"}


@programme_bp.route("/programmes/<int:programme_id>", methods=["DELETE"])
def delete_programmes(programme_id):
    affected_rows = db.session.query(Programme).filter_by(id=programme_id).delete()
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Programme with ID={programme_id} deleted"}
    else:
        return {"response": f"No programme with ID={programme_id} to delete"}
