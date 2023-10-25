from flask import Blueprint, jsonify, request
from models.ratings import Rating
from __init__ import db
from datetime import datetime
from sqlalchemy import func
from models.courses import Course
from models.subjects import Subject

rating_bp = Blueprint("ratings", __name__)


@rating_bp.route("/rating", methods=["POST"])
def insert_rating():
    data = request.get_json()
    date_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
    rating = int(data["rating"])
    room_id = int(data["room"])
    subject_id = (
        db.session.query(Course)
        .join(Subject)
        .filter(
            db.and_(
                Course.room_id == room_id,
                Course.start_end[0] <= date_time.time(),
                Course.start_end[1] >= date_time.time(),
                Course.day == date_time.weekday(),
            )
        )
        .with_entities(Course.subject_id)
        .first()
    )

    try:
        new_rating = Rating(rating, subject_id, room_id, date_time)
        db.session.add(new_rating)
        db.session.commit()
        return {"response": "New rating added to database"}
    except Exception:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@rating_bp.route("/rating/<int:subject_id>", methods=["GET"])
def get_average_rating(subject_id):
    average_rating = (
        db.session.query(func.avg(Rating.rating))
        .filter(Rating.subject_id == subject_id)
        .scalar()
    )

    return jsonify({"response": round(average_rating, 2)})


@rating_bp.route("/ratingsnumber/<int:subject_id>", methods=["GET"])
def get_ratings(subject_id):
    ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    rating_counts = (
        db.session.query(Rating.rating, func.count(Rating.rating))
        .group_by(Rating.rating)
        .all()
    )

    for rating, count in rating_counts:
        ratings[rating] = count

    ratings_dict = {f"{key}_rating": value for key, value in ratings.items()}

    return jsonify(ratings_dict)
