from flask import Blueprint, jsonify, request
from __init__ import db
from sqlalchemy import exc
from models.ratings import Rating
from models.weeks import Week
from models.subjects import Subject
from datetime import date

graph_bp = Blueprint("graph", __name__)


@graph_bp.route("/graph", methods=["GET"])
def get_graph_data():
    subject_id = request.args.get("subject_id")
    if subject_id:
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

            return jsonify(week_ratings)
        else:
            return {"response": "An error has occured. 1"}
    else:
        return {"response": "An error has occured. 2"}
