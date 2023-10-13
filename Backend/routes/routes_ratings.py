from flask import Blueprint, jsonify, request
from models.ratings import Rating
from __init__ import db
from datetime import datetime

rating_bp = Blueprint("ratings", __name__)


@rating_bp.route("/rating", methods=["POST"])
def insert_rating():
    data = request.get_json()
    date_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
    rating = int(data["rating"])
    room_id = int(data["room"])
    # subject_id = get_current_subject(date_time, room_id)
    subject_id = 2
    # try:
    new_rating = Rating(rating, subject_id, room_id, date_time)
    db.session.add(new_rating)
    db.session.commit()
    return {"response": "New rating added to database"}
    # except Exception:
    #    session.rollback()
    #    return {"response": "An error has occured"}, 404


@rating_bp.route("/rating/<int:subject_id>", methods=["GET"])
def get_average_rating(subject_id):
    average_rating = db.select(db.func.avg(Rating)).where(
        Rating.subject_id == subject_id
    )
    result = db.session.execute(average_rating).scalar()
    return {"response": result}
