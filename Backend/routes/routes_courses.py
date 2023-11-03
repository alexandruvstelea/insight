from flask import Blueprint, jsonify, request, abort
from models.courses import Course
from models.subjects import Subject
from __init__ import db
from sqlalchemy import exc
from bleach import clean

course_bp = Blueprint("courses", __name__)


@course_bp.route("/courses", methods=["POST"])
def create_course():
    try:
        subject_id = clean(request.form["subject_id"])
        type = clean(request.form["type"])
        room_id = clean(request.form["room_id"])
        day = clean(request.form["day"])
        week_type = clean(request.form["week_type"])
        start = clean(request.form["start"])
        end = clean(request.form["end"])
        start_end = [start, end]
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    try:
        with db.session.begin():
            subject = db.session.query(Subject).filter(Subject.id == subject_id).first()
            semester = 0
            if subject:
                semester = subject.semester
            else:
                abort(404, "Couldn't determine subject for course.")
            new_course = Course(
                subject_id, type, room_id, day, week_type, start_end, semester
            )
            db.session.add(new_course)
            db.session.commit()
            return {"response": "New course added to database"}, 200
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while adding object to database.\n {str(e)}")


@course_bp.route("/courses", methods=["GET"])
def get_courses():
    try:
        courses = db.session.query(Course).all()
        courses_list = []
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
        return jsonify(courses_list), 200
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving objects.\n {str(e)}")


@course_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    try:
        course = db.session.query(Course).filter(Course.id == course_id).first()
        if course:
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
            abort(404, f"No course with ID={course_id} found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving the object.\n {str(e)}")


@course_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    try:
        new_subject_id = clean(request.form["new_subject_id"])
        new_type = clean(request.form["new_type"])
        new_room_id = clean(request.form["new_room_id"])
        new_day = clean(request.form["new_day"])
        new_week_type = clean(request.form["new_week_type"])
        new_start = clean(request.form["new_start"])
        new_end = clean(request.form["new_end"])
        new_start_end = [new_start, new_end]
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    try:
        with db.session.begin():
            subject = (
                db.session.query(Subject).filter(Subject.id == new_subject_id).first()
            )
            new_semester = subject.semester if subject else 0
            if new_semester == 0:
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
                return {"response": f"Course with ID={course_id} updated."}, 200
            else:
                abort(404, f"No course with ID={course_id} to update.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while updating the object.\n {str(e)}")


@course_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        with db.session.begin():
            affected_rows = db.session.query(Course).filter_by(id=course_id).delete()
            if affected_rows > 0:
                db.session.commit()
                return {"response": f"Course with ID={course_id} deleted."}, 200
            else:
                abort(404, f"No course with ID={course_id} to delete.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while deleting the object.\n {str(e)}")
