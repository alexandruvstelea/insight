from flask import Blueprint, jsonify, request
from models.programmes_subjects import ProgrammesSubjects
from __init__ import db
from sqlalchemy import exc

programme_subjects_bp = Blueprint("programmes_subjects", __name__)


@programme_subjects_bp.route("/programmesubjects", methods=["POST"])
def create_programme_subject():
    programme_id = request.form["programme_id"]
    subject_id = request.form["subject_id"]
    new_relation = ProgrammesSubjects(programme_id, subject_id)
    try:
        db.session.add(new_relation)
        db.session.commit()
        return {"response": "New relation added to database"}
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@programme_subjects_bp.route("/programmesubjects", methods=["GET"])
def get_programmes_subjects():
    relations = db.session.query(ProgrammesSubjects).all()
    relations_list = []
    for relation in relations:
        relations_list.append(
            {
                "programme_id": relation.programme_id,
                "subject_id": relation.subject_id,
            }
        )
    return jsonify(relations_list)


@programme_subjects_bp.route(
    "/programmesubjects/<int:programme_id>/<int:subject_id>", methods=["PUT"]
)
def update_programmes_subjects(programme_id, subject_id):
    new_programme_id = request.form["new_programme_id"]
    new_subject_id = request.form["new_subject_id"]
    try:
        affected_rows = (
            db.session.querry(ProgrammesSubjects)
            .filter(
                db.and_(
                    ProgrammesSubjects.programme_id == programme_id,
                    ProgrammesSubjects.subject_id == subject_id,
                )
            )
            .update(
                {
                    "programme_id": new_programme_id,
                    "subject_id": new_subject_id,
                }
            )
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Relation [{programme_id,subject_id}] updated."}
    else:
        return {"response": f"No relation [{programme_id,subject_id}] to update."}


@programme_subjects_bp.route(
    "/programmesubjects/<int:programme_id>/<int:subject_id>", methods=["DELETE"]
)
def delete_programmes_subjects(programme_id, subject_id):
    affected_rows = (
        db.session.query(ProgrammesSubjects)
        .filter(
            db.and_(
                ProgrammesSubjects.programme_id == programme_id,
                ProgrammesSubjects.subject_id == subject_id,
            )
        )
        .delete()
    )
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Relation [{programme_id,subject_id}] deleted."}
    else:
        return {"response": f"No relation [{programme_id,subject_id}] to delete."}
