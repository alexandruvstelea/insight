from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request, abort
from models.subjects import Subject
from models.courses import Course
from __init__ import db, limiter
from datetime import datetime
from sqlalchemy import exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
course_bp = Blueprint("courses", __name__)


@course_bp.route("/courses", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def create_course():
    if current_user.user_type == 0:
        try:
            subject_id = int(clean(request.form["subject_id"]))
            type = int(clean(request.form["type"]))
            room_id = int(clean(request.form["room_id"]))
            day = int(clean(request.form["day"]))
            week_type = int(clean(request.form["week_type"]))
            start = clean(request.form["start"])
            end = clean(request.form["end"])
            start_end = [start, end]
        except KeyError as e:
            logger.error(f"An error has occured: missing key in request parameters.")
            abort(400, f"An error has occured: missing key in request parameters.")
        except ValueError as e:
            logger.error(f"An error has occurred: {e}")
            abort(400, f"An error has occurred: {e}")
        try:
            subject = db.session.query(Subject).filter(Subject.id == subject_id).first()
            semester = 0
            if subject:
                semester = subject.semester
                existing_courses = (
                    db.session.query(Course)
                    .filter(
                        Course.day == day,
                        Course.week_type == week_type,
                        Course.room_id == room_id,
                        Course.semester == semester,
                    )
                    .all()
                )
                filtered_courses = []
                for course in existing_courses:
                    if (
                        course.start_end[0] <= datetime.strptime(start, "%H:%M").time()
                        and course.start_end[1]
                        >= datetime.strptime(end, "%H:%M").time()
                    ):
                        filtered_courses.append(course)

                if filtered_courses:
                    logger.warning("A course is already scheduled in the given slot.")
                    abort(409, "A course is already scheduled in the given slot.")
            else:
                logger.warning("Couldn't determine subject for course.")
                abort(404, "Couldn't determine subject for course.")
            new_course = Course(
                subject_id, type, room_id, day, week_type, start_end, semester
            )
            db.session.add(new_course)
            db.session.commit()
            return {"response": "New course added to database"}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while adding course to database.\n {e}")
            abort(500, f"An error has occured while adding course to database.")
    abort(401, "Account not authorized to perform this action.")


@course_bp.route("/courses", methods=["GET"])
@limiter.limit("50 per minute")
def get_courses():
    try:
        courses = db.session.query(Course).all()
        courses_list = []
        if courses:
            for course in courses:
                courses_list.append(
                    {
                        "id": course.id,
                        "subject_id": course.subject_id,
                        "type": course.type,
                        "room_id": course.room_id,
                        "day": course.day,
                        "week_type": course.week_type,
                        "start": course.start_end[0].strftime("%H:%M"),
                        "end": course.start_end[1].strftime("%H:%M"),
                        "semester": course.semester,
                    }
                ), 200
            logger.info(f"Courses retrieved from database.{courses_list}")
            return jsonify(courses_list), 200
        else:
            logger.warning(f"No courses found.")
            abort(404, f"No courses found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving courses.\n{e}")
        abort(500, f"An error has occured while retrieving courses.")


@course_bp.route("/courses/<int:course_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_course_by_id(course_id):
    try:
        course = db.session.query(Course).filter(Course.id == course_id).first()
        if course:
            logger.info(f"Course retrieved from database. {course}")
            return {
                "id": course.id,
                "subject_id": course.subject_id,
                "type": course.type,
                "room_id": course.room_id,
                "day": course.day,
                "week_type": course.week_type,
                "start": course.start_end[0].strftime("%H:%M"),
                "end": course.start_end[1].strftime("%H:%M"),
                "semester": course.semester,
            }, 200
        else:
            logger.warning(f"No course with ID={course_id} found.")
            abort(404, f"No course with ID={course_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving courses.\n{e}")
        abort(500, f"An error has occured while retrieving courses.")


@course_bp.route("/courses/<int:course_id>", methods=["PUT"])
@login_required
@limiter.limit("50 per minute")
def update_course(course_id):
    if current_user.user_type == 0:
        try:
            new_subject_id = int(clean(request.form["new_subject_id"]))
            new_type = int(clean(request.form["new_type"]))
            new_room_id = int(clean(request.form["new_room_id"]))
            new_day = int(clean(request.form["new_day"]))
            new_week_type = int(clean(request.form["new_week_type"]))
            new_start = clean(request.form["new_start"])
            new_end = clean(request.form["new_end"])
            new_start_end = [new_start, new_end]
        except KeyError as e:
            logger.error(
                f"An error has occured: missing key in request parameters.\n {e}"
            )
            abort(400, f"An error has occured: missing key in request parameters.")
        except ValueError as e:
            logger.error(f"An error has occurred: {e}")
            abort(400, f"An error has occurred: {e}")
        try:
            subject = (
                db.session.query(Subject).filter(Subject.id == new_subject_id).first()
            )
            new_semester = subject.semester if subject else 0
            if new_semester == 0:
                logger.error("Couldn't determine subject for course.")
                abort(404, "Couldn't determine subject for course.")
            affected_rows = (
                db.session.query(Course)
                .filter_by(id=course_id)
                .update(
                    {
                        "subject_id": new_subject_id,
                        "type": new_type,
                        "room_id": new_room_id,
                        "day": new_day,
                        "week_type": new_week_type,
                        "start_end": new_start_end,
                        "semester": new_semester,
                    }
                )
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Course with ID={course_id} updated.")
                return {"response": f"Course with ID={course_id} updated."}, 200
            else:
                logger.warning(f"No course with ID={course_id} to update.")
                abort(404, f"No course with ID={course_id} to update.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while updating course.\n {e}")
            abort(500, f"An error has occured while updating course.")
    abort(401, "Account not authorized to perform this action.")


@course_bp.route("/courses/<int:course_id>", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def delete_course(course_id):
    if current_user.user_type == 0:
        try:
            affected_rows = db.session.query(Course).filter_by(id=course_id).delete()
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Course with ID={course_id} deleted.")
                return {"response": f"Course with ID={course_id} deleted."}, 200
            else:
                logger.warning(f"No course with ID={course_id} to delete.")
                abort(404, f"No course with ID={course_id} to delete.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while deleting course.\n {e}")
            abort(500, f"An error has occured while deleting course.")
    abort(401, "Account not authorized to perform this action.")
