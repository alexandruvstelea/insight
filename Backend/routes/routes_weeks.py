from flask import Blueprint, jsonify, request, abort
from models.weeks import Week
from __init__ import db, limiter
from sqlalchemy import text, exc
from datetime import timedelta, datetime
from bleach import clean
from flask_jwt_extended import jwt_required

weeks_bp = Blueprint("weeks", __name__)


@weeks_bp.route("/weeks", methods=["POST"])
@jwt_required()
@limiter.limit("50 per minute")
def generate_weeks():
    try:
        year_start = datetime.strptime(clean(request.form["year_start"]), "%Y-%m-%d")
        intervals = [int(i) for i in request.form.getlist("intervals")]
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")

    def add_weeks(number_of_weeks, interval_start, counter):
        try:
            with db.session.begin():
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
        except Exception as e:
            abort(500, f"An error has occured while generating weeks.\n {str(e)}")

    try:
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

        return {"response": "Weeks generated"}, 200
    except Exception as e:
        abort(500, f"An error has occured while generating weeks.\n {str(e)}")


@weeks_bp.route("/weeks", methods=["GET"])
@limiter.limit("50 per minute")
def get_weeks():
    try:
        weeks = db.session.query(Week).all()
        weeks_list = []
        if weeks:
            for week in weeks:
                weeks_list.append(
                    {
                        "id": week.id,
                        "start": week.start,
                        "end": week.end,
                        "semester": week.semester,
                    }
                )
            return jsonify(weeks_list), 200
        else:
            abort(404, "No weeks found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving data.\n {str(e)}")


@weeks_bp.route("/weeks", methods=["DELETE"])
@jwt_required()
@limiter.limit("50 per minute")
def reset_weeks():
    try:
        with db.session.begin():
            db.session.execute(text('TRUNCATE TABLE "Weeks" RESTART IDENTITY;'))
            db.session.commit()
            return {"response": "Weeks deleted from database."}, 200
    except exc.SQLAlchemyError as e:
        return abort(500, f"An error has occured while deleting objects.\n {str(e)}")
