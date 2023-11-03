from flask import Blueprint, jsonify, request, abort
from models.subjects import Subject
from __init__ import db
from sqlalchemy import exc
from datetime import datetime
from models.courses import Course
from models.weeks import Week

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


@subject_bp.route("/subjects/current", methods=["GET"])
def get_current_subject():
    try:
        data = request.get_json()
        if not data:
            abort(400, "Invalid JSON data provided.")
        date_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
        room_id = int(data["room"])
    except (KeyError, ValueError, TypeError) as e:
        abort(400, f"Error retrieving query parameters: {str(e)}")

    try:
        week_type = find_week_type(date_time)
        courses = (
            db.session.query(Course)
            .filter(
                Course.room_id == room_id,
                Course.day == date_time.weekday(),
                db.or_(Course.week_type == week_type, Course.week_type == 0),
            )
            .all()
        )

        filtered_courses = []
        if courses:
            for course in courses:
                if course.start_end[0] <= date_time.time() <= course.start_end[1]:
                    filtered_courses.append(course)

            if len(filtered_courses) == 1:
                subject_id = filtered_courses[0].id
                subject = db.session.query(Subject).filter_by(id=subject_id).first()
                if subject:
                    return {
                        "name": subject.name,
                        "abbreviation": subject.abbreviation,
                    }, 200
                else:
                    abort(500, f"Subject with ID={subject_id} not found.")
            else:
                abort(404, "Current course not found.")
        else:
            abort(404, "No courses found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"Error retrieving data: {str(e)}")


def find_week_type(date_time):
    current_week = (
        db.session.query(Week)
        .filter(Week.start <= date_time, Week.end >= date_time)
        .first()
    )
    if current_week:
        return 2 if current_week.id % 2 == 0 else 1
    else:
        abort(404, "Current week couldn't be determined.")
