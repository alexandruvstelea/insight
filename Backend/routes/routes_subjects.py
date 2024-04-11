from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from models.professors import Professor
from models.programmes import Programme
from models.subjects import Subject
from routes.helpers import find_week_type
from models.courses import Course
from __init__ import db, limiter
from datetime import datetime
from sqlalchemy import exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
subject_bp = Blueprint("subjects", __name__)


@subject_bp.route("/subjects", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def create_subject():
    if current_user.user_type == 0:
        try:
            name = clean(request.form.get("name"))
            abbreviation = clean(request.form.get("abbreviation"))
            professor_id = clean(request.form.get("professor_id"))
            semester = clean(request.form.get("semester"))
            programme_ids = [int(i) for i in request.form.getlist("programme_ids")]
            new_subject = Subject(name, abbreviation, professor_id, semester)
            db.session.add(new_subject)
            db.session.commit()
            for pid in programme_ids:
                programme = db.session.query(Programme).filter_by(id=pid).first()
                if programme:
                    new_subject.programmes.append(programme)
            db.session.commit()
            return {"response": "New subject added to database"}, 200
        except (ValueError, TypeError) as e:
            logger.error(f"An error has occured: request parameters not ok.\n{e}")
            abort(400, f"An error has occured: request parameters not ok.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@subject_bp.route("/subjects", methods=["GET"])
@limiter.limit("50 per minute")
def get_subjects():
    try:
        subjects = db.session.query(Subject).all()
        subjects_list = []
        if subjects:
            for subject in subjects:
                subjects_list.append(
                    {
                        "id": subject.id,
                        "name": subject.name,
                        "abbreviation": subject.abbreviation,
                        "professor_id": subject.professor_id,
                        "semester": subject.semester,
                        "programmes": [
                            {"id": p.id, "name": p.name} for p in subject.programmes
                        ],
                    }
                )
            logger.info(f"Retrieved subjects list from database.{subjects_list}")
            return jsonify(subjects_list), 200
        else:
            logger.warning("No subjects found.")
            abort(404, "No subjects found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@subject_bp.route("/subjects/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_subject_by_id(subject_id):
    try:
        subject = db.session.query(Subject).filter_by(id=subject_id).first()
        if subject:
            logger.info(f"Retrieved subject from database.{subject}")
            return {
                "id": subject.id,
                "name": subject.name,
                "abbreviation": subject.abbreviation,
                "professor_id": subject.professor_id,
                "semester": subject.semester,
                "programmes": [
                    {"id": p.id, "name": p.name} for p in subject.programmes
                ],
            }, 200
        else:
            logger.warning(f"No subject with ID={subject_id} found.")
            return abort(404, f"No subject with ID={subject_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@subject_bp.route("/subjects/<int:subject_id>", methods=["PUT"])
@login_required
@limiter.limit("50 per minute")
def update_subject(subject_id):
    if current_user.user_type == 0:
        try:
            new_name = clean(request.form.get("new_name"))
            new_abbreviation = clean(request.form.get("new_abbreviation"))
            new_professor_id = clean(request.form.get("new_professor_id"))
            new_semester = clean(request.form.get("new_semester"))
            programme_ids = [int(i) for i in request.form.getlist("programme_ids")]
            subject = db.session.query(Subject).filter_by(id=subject_id).first()
            if not subject:
                abort(404, f"No subject with ID={subject_id} to update")
            subject.name = new_name
            subject.abbreviation = new_abbreviation
            subject.professor_id = new_professor_id
            subject.semester = new_semester
            new_programmes = (
                db.session.query(Programme)
                .filter(Programme.id.in_(programme_ids))
                .all()
            )
            subject.programmes = new_programmes
            db.session.commit()
            logger.info(f"Subject with ID={subject_id} updated")
            return {"response": f"Subject with ID={subject_id} updated"}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@subject_bp.route("/subjects/<int:subject_id>", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def delete_subjects(subject_id):
    if current_user.user_type == 0:
        try:
            subject = db.session.query(Subject).filter_by(id=subject_id).first()
            if subject:
                for programme in subject.programmes:
                    programme.subjects.remove(subject)
                db.session.delete(subject)
                db.session.commit()
                logger.info(f"Subject with ID={subject_id} deleted")
                return {"response": f"Subject with ID={subject_id} deleted"}, 200
            else:
                logger.warning(f"No subject with ID={subject_id} to delete")
                return abort(404, f"No subject with ID={subject_id} to delete")

        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@subject_bp.route("/subjects/professor/<int:professor_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_professor_subjects(professor_id):
    try:
        subjects = db.session.query(Subject).filter_by(professor_id=professor_id)
        subjects_list = []
        if subjects:
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
            subjects_list.sort(key=lambda subj: subj["name"])
            logger.info(f"Retrieved subjects list. {subjects_list}")
            return jsonify(subjects_list), 200
        else:
            logger.warning("No subjects found.")
            abort(404, "No subjects found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@subject_bp.route("/subjects/description/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_subject_description(subject_id):
    try:
        subject = db.session.query(Subject).filter_by(id=subject_id).first()
        if subject.professor_id:
            professor = (
                db.session.query(Professor).filter_by(id=subject.professor_id).first()
            )
        if professor:
            if professor.last_name == "Cațaron" or professor.last_name == "Danciu":
                return {
                    "subject_name": subject.name,
                    "professor_name": f"{professor.last_name} {professor.first_name} 😎",
                }
            return {
                "subject_name": subject.name,
                "professor_name": f"{professor.last_name} {professor.first_name}",
            }
        else:
            abort(404, "Subject details not found!")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@subject_bp.route("/subjects/current", methods=["POST"])
@limiter.limit("50 per minute")
def get_current_subject():
    try:
        data = request.get_json()
        if not data:
            logger.error("Invalid JSON data provided.")
            abort(400, "Invalid JSON data provided.")
        date_time = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S.%f")
        room_id = int(data.get("room"))
        week_type, semester = find_week_type(date_time)
        if week_type == False:
            abort(404, "Current week couldn't be determined.")
        courses = (
            db.session.query(Course)
            .filter(
                Course.room_id == room_id,
                Course.day == date_time.weekday(),
                Course.semester == semester,
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
                subject_id = filtered_courses[0].subject_id
                subject = db.session.query(Subject).filter_by(id=subject_id).first()
                if subject:
                    logger.info(f"Retrieved current subject.{subject}")
                    return {
                        "name": subject.name,
                        "abbreviation": subject.abbreviation,
                    }, 200
                else:
                    logger.warning(f"Subject with ID={subject_id} not found.")
                    abort(404, f"Subject with ID={subject_id} not found.")
            else:
                logger.warning("Current course not found.")
                abort(404, "Current course not found.")
        else:
            logger.warning("No courses found.")
            abort(404, "No courses found.")
    except (ValueError, TypeError) as e:
        logger.error(f"An error has occured: request parameters not ok.\n{e}")
        abort(400, f"An error has occured: request parameters not ok.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")
