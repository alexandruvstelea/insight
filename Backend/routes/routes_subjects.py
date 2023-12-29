from flask import Blueprint, jsonify, request, abort
from models.subjects import Subject
from models.comments import Comment
from __init__ import db, limiter
from sqlalchemy import exc
from datetime import datetime
from models.courses import Course
from models.weeks import Week
from bleach import clean
from models.ratings import Rating
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger(__name__)
subject_bp = Blueprint("subjects", __name__)


@subject_bp.route("/subjects", methods=["POST"])
@jwt_required()
@limiter.limit("50 per minute")
def create_subject():
    try:
        name = clean(request.form["name"])
        abbreviation = clean(request.form["abbreviation"])
        professor_id = clean(request.form["professor_id"])
        semester = clean(request.form["semester"])
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    new_subject = Subject(name, abbreviation, professor_id, semester)
    try:
        with db.session.begin():
            db.session.add(new_subject)
            db.session.commit()
            # logger.info(f"New subject added to database.{new_subject}")
            return {"response": "New subject added to database"}, 200
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while adding obejct to database.\n {e}")
        return abort(500, f"An error has occured while adding obejct to database.")


@subject_bp.route("/subjects", methods=["GET"])
@limiter.limit("50 per minute")
def get_subject():
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
                    }
                )
            logger.info(f"Retrieved subjects list from database.{subjects_list}")
            return jsonify(subjects_list), 200
        else:
            logger.warning("No subjects found.")
            abort(404, "No subjects found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving objects.\n {e}")
        abort(500, f"An error has occured while retrieving objects.")


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
            }, 200
        else:
            logger.warning(f"No subject with ID={subject_id} found.")
            return abort(404, f"No subject with ID={subject_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving objects.\n {e}")
        abort(500, f"An error has occured while retrieving objects.")


@subject_bp.route("/subjects/sentiment/<int:subject_id>", methods=["GET"])
def get_subject_sentiment(subject_id):
    try:
        comments_sentiment = (
            db.session.query(Comment.sentiment)
            .filter(Comment.sentiment != -2, Comment.sentiment != 0)
            .all()
        )
        if comments_sentiment:
            total_count = len(comments_sentiment)
            positive_count = sum(
                1 for sentiment in comments_sentiment if sentiment[0] == 1
            )
            negative_count = sum(
                1 for sentiment in comments_sentiment if sentiment[0] == -1
            )
            positive_percentage = (
                (positive_count / total_count) * 100 if total_count > 0 else 0
            )
            negative_percentage = (
                (negative_count / total_count) * 100 if total_count > 0 else 0
            )
            return {
                "positive": positive_percentage,
                "negative": negative_percentage,
            }
        else:
            logger.warning(f"No comments found for subject with ID={subject_id}.")
            return abort(404, f"No comments found for subject with ID={subject_id}.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving data.\n {e}")
        abort(500, f"An error has occured while retrieving data.")


@subject_bp.route("/subjects/<int:subject_id>", methods=["PUT"])
@jwt_required()
@limiter.limit("50 per minute")
def update_subject(subject_id):
    try:
        new_name = clean(request.form["new_name"])
        new_abbreviation = clean(request.form["new_abbreviation"])
        new_professor_id = clean(request.form["new_professor_id"])
        new_semester = clean(request.form["new_semester"])
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    try:
        with db.session.begin():
            subject = db.session.query(Subject).filter_by(id=subject_id).first()
            if subject.semester != new_semester:
                db.session.query(Course).filter(Course.subject_id == subject_id).update(
                    {"semester": new_semester}
                )
                db.session.query(Rating).filter_by(subject_id=subject_id).delete()
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

            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Subject with ID={subject_id} updated")
                return {"response": f"Subject with ID={subject_id} updated"}, 200
            else:
                logger.warning(f"No subject with ID={subject_id} to update")
                return abort(404, f"No subject with ID={subject_id} to update")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving objects.\n {e}")
        abort(500, f"An error has occured while retrieving objects.")


@subject_bp.route("/subjects/<int:subject_id>", methods=["DELETE"])
@jwt_required()
@limiter.limit("50 per minute")
def delete_subjects(subject_id):
    try:
        with db.session.begin():
            affected_rows = db.session.query(Subject).filter_by(id=subject_id).delete()
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Subject with ID={subject_id} deleted")
                return {"response": f"Subject with ID={subject_id} deleted"}, 200
            else:
                logger.warning(f"No subject with ID={subject_id} to delete")
                return abort(404, f"No subject with ID={subject_id} to delete")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while deleting objects.\n {e}")
        abort(500, f"An error has occured while deleting objects.")


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
            logger.info(f"Retrieved subjects list. {subjects_list}")
            return jsonify(subjects_list), 200
        else:
            logger.warning("No subjects found.")
            abort(404, "No subjects found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving objects.\n {e}")
        abort(500, f"An error has occured while retrieving objects.")


@subject_bp.route("/subjects/current", methods=["GET"])
@limiter.limit("50 per minute")
def get_current_subject():
    try:
        data = request.get_json()
        if not data:
            logger.error("Invalid JSON data provided.")
            abort(400, "Invalid JSON data provided.")
        date_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
        room_id = int(data["room"])
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error retrieving query parameters: {str(e)}")
        abort(400, f"Error retrieving query parameters.")

    try:
        week_type, semester = find_week_type(date_time)
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
    except exc.SQLAlchemyError as e:
        logger.error(f"Error retrieving data: {str(e)}")
        abort(500, f"Error retrieving data.")


def find_week_type(date_time):
    current_week = (
        db.session.query(Week)
        .filter(Week.start <= date_time, Week.end >= date_time)
        .first()
    )
    logger.info(f"{date_time}")
    if current_week:
        logger.info("Retrieved current week type.")
        return (
            [2, current_week.semester]
            if current_week.id % 2 == 0
            else [1, current_week.semester]
        )
    else:
        logger.error("Current week couldn't be determined.")
        abort(404, "Current week couldn't be determined.")
