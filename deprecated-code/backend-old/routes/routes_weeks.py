from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from datetime import timedelta, datetime
from __init__ import db, limiter
from models.weeks import Week
from sqlalchemy import text, exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
weeks_bp = Blueprint("weeks", __name__)


@weeks_bp.route("/weeks", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def generate_weeks():
    if current_user.user_type == 0:
        try:
            year_start = datetime.strptime(
                clean(request.form.get("year_start")), "%Y-%m-%d"
            )
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
            logger.info("Generated weeks.")
            return {"response": "Weeks generated"}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@weeks_bp.route("/weeks", methods=["GET"])
@limiter.limit("50 per minute")
def get_weeks():
    try:
        weeks = db.session.query(Week).all()
        if weeks:
            weeks_list = []
            for week in weeks:
                weeks_list.append(
                    {
                        "id": week.id,
                        "start": week.start,
                        "end": week.end,
                        "semester": week.semester,
                    }
                )
            logger.info(f"Retrieved weeks list. {weeks_list}")
            return jsonify(weeks_list), 200
        else:
            logger.warning("No weeks found.")
            abort(404, "No weeks found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@weeks_bp.route("/weeks", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def reset_weeks():
    if current_user.user_type == 0:
        try:
            db.session.execute(text('TRUNCATE TABLE "Weeks" RESTART IDENTITY;'))
            db.session.commit()
            logger.info("Weeks deleted from database.")
            return {"response": "Weeks deleted from database."}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")
