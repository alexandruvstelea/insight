from flask import Blueprint, jsonify, request
from models.subjects import Subject
from __init__ import db
from sqlalchemy import exc

subject_bp = Blueprint("subjects", __name__)


@subject_bp.route("/subjects", methods=["POST"])
def create_subject():
    name = request.form["name"]
    abbreviation = request.form["abbreviation"]
    professor_id = request.form["professor_id"]
    semester = request.form["semester"]
    new_subject = Subject(name, abbreviation, professor_id, semester)
    try:
        db.session.add(new_subject)
        db.session.commit()
        return {"response": "New subject added to database"}
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@subject_bp.route("/subjects", methods=["GET"])
def get_subject():
    subjects = db.session.query(Subject).all()
    subjects_list = []
    for subject in subjects:
        subjects_list.append(
            {
                "id": subject.id,
                "name": subject.name,
                "abbreviation": subject.abbreviation,
                "professor_id": subject.professor_id,
                "semester": subject.semester,
            }
        )
    return jsonify(subjects_list)


@subject_bp.route("/subjects/<int:subject_id>", methods=["GET"])
def get_subject_by_id(subject_id):
    subject = db.session.query(Subject).filter_by(id=subject_id).first()
    if subject:
        return {
            "id": subject.id,
            "name": subject.name,
            "abbreviation": subject.abbreviation,
            "professor_id": subject.professor_id,
            "semester": subject.semester,
        }
    else:
        return {"response": f"No subject with ID={subject_id} found."}


@subject_bp.route("/subjects/<int:subject_id>", methods=["PUT"])
def update_subject(subject_id):
    new_name = request.form["new_name"]
    new_abbreviation = request.form["new_abbreviation"]
    new_professor_id = request.form["new_professor_id"]
    new_semester = request.form["new_semester"]
    try:
        affected_rows = (
            db.session.query(Subject)
            .filter_by(id=subject_id)
            .update(
                {
                    "name": new_name,
                    "abbreviation": new_abbreviation,
                    "professor_id": new_professor_id,
                    "semester": new_semester,
                }
            )
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Subject with ID={subject_id} updated"}
    else:
        return {"response": f"No subject with ID={subject_id} to update"}


@subject_bp.route("/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subjects(subject_id):
    affected_rows = db.session.query(Subject).filter_by(id=subject_id).delete()
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Subject with ID={subject_id} deleted"}
    else:
        return {"response": f"No subject with ID={subject_id} to delete"}


@subject_bp.route("/subjects/professor/<int:professor_id>", methods=["GET"])
def get_professor_subjects(professor_id):
    subjects = db.session.query(Subject).filter_by(professor_id=professor_id)
    subjects_list = []
    for subject in subjects:
        subjects_list.append(
            {
                "id": subject.id,
                "name": subject.name,
                "abbreviation": subject.abbreviation,
                "professor_id": subject.professor_id,
                "semester": subject.semester,
            }
        )
    return jsonify(subjects_list)
