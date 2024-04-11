from flask import Blueprint, jsonify, request, abort
from routes.helpers import verify_code, last_three_digits
from flask_login import login_required, current_user
from models.subjects import Subject
from models.ratings import Rating
from sqlalchemy import func, exc
from __init__ import db, limiter
from datetime import datetime
from models.weeks import Week
from bleach import clean
import logging

logger = logging.getLogger(__name__)
rating_bp = Blueprint("ratings", __name__)


@rating_bp.route("/rating", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def insert_rating():
    try:
        date_time = datetime.strptime(
            clean(request.form.get("date")), "%Y-%m-%d %H:%M:%S.%f"
        )
        rating_clarity = int(clean(request.form.get("clarity")))
        rating_interactivity = int(clean(request.form.get("interactivity")))
        rating_relevance = int(clean(request.form.get("relevance")))
        rating_comprehension = int(clean(request.form.get("comprehension")))
        room_id = int(clean(request.form.get("room_id")))
        code = int(clean(request.form.get("code")))
        if verify_code(room_id, code):
            subject_id = last_three_digits(code)
            subject = db.session.query(Subject).filter_by(id=subject_id).first()
            subject_programmes = [programme.id for programme in subject.programmes]
            if current_user.programme_id in subject_programmes:
                rating_overall = (
                    rating_clarity
                    + rating_interactivity
                    + rating_relevance
                    + rating_comprehension
                ) / 4

                new_rating = Rating(
                    rating_clarity,
                    rating_interactivity,
                    rating_relevance,
                    rating_comprehension,
                    rating_overall,
                    subject_id,
                    date_time,
                )
                db.session.add(new_rating)
                db.session.commit()
                return {"response": "New rating added to database."}
            else:
                logger.info("User programme doesn't match subject programme.")
                abort(400, "User programme doesn't match subject programme.")
        abort(400, "Invalid code.")
    except (ValueError, TypeError) as e:
        logger.error(f"An error has occured: request parameters not ok.\n{e}")
        abort(400, f"An error has occured: request parameters not ok.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@rating_bp.route("/rating/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_average_ratings(subject_id):
    try:
        average_ratings = (
            db.session.query(
                func.avg(Rating.rating_clarity).label("clarity"),
                func.avg(Rating.rating_interactivity).label("interactivity"),
                func.avg(Rating.rating_relevance).label("relevance"),
                func.avg(Rating.rating_comprehension).label("comprehension"),
                func.avg(Rating.rating_overall).label("overall"),
            )
            .filter(Rating.subject_id == subject_id)
            .one()
        )
        if (
            average_ratings.clarity
            and average_ratings.interactivity
            and average_ratings.relevance
            and average_ratings.comprehension
            and average_ratings.overall
        ):
            logger.info(
                f"Calculated and returned average rating for subject with ID={subject_id}"
            )
            return jsonify(
                {
                    "clarity": round(average_ratings.clarity, 1),
                    "interactivity": round(average_ratings.interactivity, 1),
                    "relevance": round(average_ratings.relevance, 1),
                    "comprehension": round(average_ratings.comprehension, 1),
                    "overall": round(average_ratings.overall, 1),
                }
            )
        else:
            logger.warning("No average ratings found.")
            abort(404, "No average ratings found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@rating_bp.route("/graph", methods=["GET"])
@limiter.limit("50 per minute")
def get_graph_data():
    try:
        subject_id = int(clean(request.args.get("subject_id")))
        subject = db.session.query(Subject).filter(Subject.id == subject_id).first()
        ratings = db.session.query(Rating).filter_by(subject_id=subject_id).all()
        if subject:
            weeks = db.session.query(Week).filter_by(semester=subject.semester).all()

        if ratings and weeks:
            week_ratings = {}
            for week in weeks:
                week_key = f"week_{week.id}"
                week_ratings[week_key] = {
                    "clarity": [],
                    "interactivity": [],
                    "relevance": [],
                    "comprehension": [],
                    "overall": [],
                }

                for rating in ratings:
                    if week.start <= rating.datetime.date() <= week.end:
                        week_ratings[week_key]["clarity"].append(rating.rating_clarity)
                        week_ratings[week_key]["interactivity"].append(
                            rating.rating_interactivity
                        )
                        week_ratings[week_key]["relevance"].append(
                            rating.rating_relevance
                        )
                        week_ratings[week_key]["comprehension"].append(
                            rating.rating_comprehension
                        )
                        week_ratings[week_key]["overall"].append(rating.rating_overall)
                for category in [
                    "clarity",
                    "interactivity",
                    "relevance",
                    "comprehension",
                    "overall",
                ]:
                    if week_ratings[week_key][category]:
                        average = sum(week_ratings[week_key][category]) / len(
                            week_ratings[week_key][category]
                        )
                        week_ratings[week_key][category] = round(average, 1)
                    else:
                        week_ratings[week_key][category] = 0

            logger.info(f"Retrieved week ratings for subject with ID={subject_id}")
            return jsonify(week_ratings), 200
        else:
            logger.warning("Couldn't find ratings.")
            return abort(404, "Couldn't find ratings.")
    except (ValueError, TypeError) as e:
        logger.error(f"An error has occured: request parameters not ok.\n{e}")
        abort(400, f"An error has occured: request parameters not ok.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")
