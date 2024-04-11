from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from models.professors import Professor
from models.subjects import Subject
from models.ratings import Rating
from __init__ import db, limiter
from sqlalchemy import exc, func
from bleach import clean
import logging

logger = logging.getLogger(__name__)
professor_bp = Blueprint("professors", __name__)


@professor_bp.route("/professors", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def create_professor():
    if current_user.user_type == 0:
        try:
            first_name = clean(request.form.get("first_name"))
            last_name = clean(request.form.get("last_name"))
            gender = clean(request.form.get("gender"))
            if gender not in ["male", "female"]:
                logger.error(
                    "Invalid gender provided. Gender must be 'male' or 'female'."
                )
                raise ValueError(
                    "Invalid gender provided. Gender must be 'male' or 'female'."
                )
            new_professor = Professor(first_name, last_name, gender)
            db.session.add(new_professor)
            db.session.commit()
            return {"response": "New professor added to database"}, 200
        except (ValueError, TypeError) as e:
            logger.error(f"An error has occured: request parameters not ok.\n{e}")
            abort(400, f"An error has occured: request parameters not ok.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@professor_bp.route("/professors", methods=["GET"])
@limiter.limit("50 per minute")
def get_professors():
    try:
        professors = db.session.query(Professor).all()
        professors_list = []
        if professors:
            for professor in professors:
                professors_list.append(
                    {
                        "id": professor.id,
                        "first_name": professor.first_name,
                        "last_name": professor.last_name,
                        "gender": professor.gender,
                    }
                )
            professors_list.sort(key=lambda prof: prof["first_name"])
            logger.info(f"Professors retrieved from database.{professors_list}")
            return jsonify(professors_list), 200
        else:
            logger.warning(f"An error has occured: no professors found.")
            abort(404, "No professors found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@professor_bp.route("/professors/<int:professor_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_professor_by_id(professor_id):
    try:
        professor = db.session.query(Professor).filter_by(id=professor_id).first()
        if professor:
            logger.info(f"Professor retrieved from database. {professor}")
            return {
                "id": professor.id,
                "first_name": professor.first_name,
                "last_name": professor.last_name,
                "gender": professor.gender,
            }, 200
        else:
            logger.warning(f"No professor with ID={professor_id} found.")
            return abort(404, f"No professor with ID={professor_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@limiter.limit("500 per minute")
@professor_bp.route("/professors/average/<int:professor_id>", methods=["GET"])
def get_professor_average(professor_id):
    try:
        professor_subjects = (
            db.session.query(Subject).filter_by(professor_id=professor_id).all()
        )
        ratings_list = []
        if professor_subjects:
            for subject in professor_subjects:
                ratings_average = (
                    db.session.query(func.avg(Rating.rating_overall))
                    .filter(Rating.subject_id == subject.id)
                    .scalar()
                )
                if ratings_average is not None:
                    ratings_list.append(round(float(ratings_average), 1))
            if ratings_list:
                return {"average": round(sum(ratings_list) / len(ratings_list), 1)}
            else:
                logger.warning(f"No ratings found for subject with ID={subject.id}.")
                abort(404, f"No ratings found for subject with ID={subject.id}.")
        else:
            logger.warning(f"No subjects found for professor with ID={professor_id}.")
            abort(404, f"No subjects found for professor with ID={professor_id}.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@professor_bp.route("/professors/<int:professor_id>", methods=["PUT"])
@login_required
@limiter.limit("50 per minute")
def update_professor(professor_id):
    if current_user.user_type == 0:
        try:
            new_first_name = clean(request.form.get("new_first_name"))
            new_last_name = clean(request.form.get("new_last_name"))
            new_gender = clean(request.form.get("new_gender"))
            if new_gender not in ["male", "female"]:
                logger.error(
                    "Invalid gender provided. Gender must be 'male' or 'female'."
                )
                raise ValueError(
                    "Invalid gender provided. Gender must be 'male' or 'female'."
                )
            affected_rows = (
                db.session.query(Professor)
                .filter_by(id=professor_id)
                .update(
                    {
                        "first_name": new_first_name,
                        "last_name": new_last_name,
                        "gender": new_gender,
                    }
                )
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Professor with ID={professor_id} updated")
                return {"response": f"Professor with ID={professor_id} updated"}, 200
            else:
                logger.warning(f"No professor with ID={professor_id} to update")
                return abort(404, f"No professor with ID={professor_id} to update")
        except (ValueError, TypeError) as e:
            logger.error(f"An error has occured: request parameters not ok.\n{e}")
            abort(400, f"An error has occured: request parameters not ok.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@professor_bp.route("/professors/<int:professor_id>", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def delete_professor(professor_id):
    if current_user.user_type == 0:
        try:
            affected_rows = (
                db.session.query(Professor).filter_by(id=professor_id).delete()
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Professor with ID={professor_id} deleted")
                return {"response": f"Professor with ID={professor_id} deleted"}, 200
            else:
                logger.warning(f"No professor with ID={professor_id} to delete")
                return abort(404, f"No professor with ID={professor_id} to delete")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")
