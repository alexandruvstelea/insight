from flask import Blueprint, jsonify, request, abort
from models.ratings import Rating
from __init__ import db, limiter
from datetime import datetime
from sqlalchemy import func, exc
from models.courses import Course
from models.subjects import Subject
from models.weeks import Week
from bleach import clean

rating_bp = Blueprint("ratings", __name__)


@rating_bp.route("/rating", methods=["POST"])
@limiter.limit("50 per minute")
def insert_rating():
    try:
        data = request.get_json()
        date_time = datetime.strptime(clean(data["date"]), "%Y-%m-%d %H:%M:%S.%f")
        rating = int(data["rating"])
        room_id = int(data["room"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")

    try:
        with db.session.begin():
            current_week = (
                db.session.query(Week)
                .filter(Week.start <= date_time, Week.end >= date_time)
                .first()
            )
            if current_week:
                current_semester = current_week.semester
            else:
                abort(404, "Could't determine current week.")
            courses = (
                db.session.query(Course)
                .filter(
                    Course.day == date_time.weekday(),
                    Course.room_id == room_id,
                    Course.semester == current_semester,
                )
                .all()
            )
            desired_time = date_time.time()
            filtered_courses = []
            if courses:
                for course in courses:
                    if (
                        course.start_end[0] <= desired_time
                        and course.start_end[1] >= desired_time
                    ):
                        filtered_courses.append(course)

                if len(filtered_courses) == 1:
                    try:
                        new_rating = Rating(
                            rating, filtered_courses[0].subject_id, date_time
                        )
                        db.session.add(new_rating)
                        db.session.commit()
                        return {"response": "New rating added to database."}
                    except exc.SQLAlchemyError as e:
                        abort(
                            500,
                            f"An error has occured while adding object to database.\n {str(e)}",
                        )
                else:
                    abort(404, "No matching course found.")
            else:
                abort(404, "No courses found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while adding object to database.\n {str(e)}")


@rating_bp.route("/rating/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_average_rating(subject_id):
    try:
        average_rating = (
            db.session.query(func.avg(Rating.rating))
            .filter(Rating.subject_id == subject_id)
            .scalar()
        )

        return jsonify({"response": round(average_rating, 2)})
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")


@rating_bp.route("/ratingsnumber/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_ratings(subject_id):
    ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    try:
        rating_counts = (
            db.session.query(Rating.rating, func.count(Rating.rating))
            .filter(Rating.subject_id == subject_id)
            .group_by(Rating.rating)
            .all()
        )

        if rating_counts:
            for rating, count in rating_counts:
                ratings[rating] = count

            ratings_dict = {f"{key}_rating": value for key, value in ratings.items()}

            return jsonify(ratings_dict), 200
        else:
            abort(404, "No ratings found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")


@rating_bp.route("/graph", methods=["GET"])
@limiter.limit("50 per minute")
def get_graph_data():
    try:
        subject_id = clean(request.args.get("subject_id"))
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    try:
        subject = db.session.query(Subject).filter(Subject.id == subject_id).first()
        ratings = db.session.query(Rating).filter_by(subject_id=subject_id).all()
        if subject:
            weeks = db.session.query(Week).filter_by(semester=subject.semester).all()

        if ratings and weeks:
            week_ratings = {}
            for week in weeks:
                week_ratings[f"week_{week.id}"] = []
                for rating in ratings:
                    if week.start <= rating.datetime.date() <= week.end:
                        week_ratings[f"week_{week.id}"].append(rating.rating)

                if week_ratings[f"week_{week.id}"]:
                    week_ratings[f"week_{week.id}"] = round(
                        sum(week_ratings[f"week_{week.id}"])
                        / len(week_ratings[f"week_{week.id}"]),
                        2,
                    )
                else:
                    week_ratings[f"week_{week.id}"] = 0

            return jsonify(week_ratings), 200
        else:
            return abort(404, "Couln't find ratings.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")
