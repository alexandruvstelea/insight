from flask import Blueprint, jsonify, request
from models.weeks import Week
from __init__ import db
from sqlalchemy import exc
from datetime import timedelta, datetime

weeks_bp = Blueprint("weeks", __name__)


@weeks_bp.route("/weeks", methods=["POST"])
def generate_weeks():
    year_start = datetime.strptime(request.form["year_start"], "%Y-%m-%d")
    intervals = [int(i) for i in request.form.getlist("intervals")]

    def add_weeks(number_of_weeks, interval_start, counter):
        for x in range(number_of_weeks):
            counter += 1
            if counter <= 14:
                semester = 1
            else:
                semester = 2
            end = interval_start + timedelta(days=6)
            db.session.add(Week(interval_start, end, semester))
            interval_start = end + timedelta(days=1)
        db.session.commit()
        return interval_start, counter

    counter = 0
    interval_start = year_start
    interval_start, counter = add_weeks(intervals[0], interval_start, counter)
    interval_start += timedelta(days=intervals[1] * 7)
    interval_start, counter = add_weeks(intervals[2], interval_start, counter)
    interval_start += timedelta(days=intervals[3] * 7)
    interval_start += timedelta(days=intervals[4] * 7)
    interval_start, counter = add_weeks(intervals[5], interval_start, counter)
    interval_start += timedelta(days=intervals[6] * 7)
    interval_start, counter = add_weeks(intervals[7], interval_start, counter)

    return {"response": "Weeks generated"}
