from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from models.programmes import Programme
from __init__ import db, limiter
from sqlalchemy import exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
programme_bp = Blueprint("programmes", __name__)


@programme_bp.route("/programmes", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def create_programme():
    if current_user.user_type == 0:
        try:
            name = clean(request.form.get("name"))
            abbreviation = clean(request.form.get("abbreviation"))
            new_programme = Programme(name, abbreviation)
            db.session.add(new_programme)
            db.session.commit()
            logger.info("New programme added to database")
            return {"response": "New programme added to database"}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@programme_bp.route("/programmes", methods=["GET"])
@limiter.limit("50 per minute")
def get_programmes():
    try:
        programmes = db.session.query(Programme).all()
        if programmes:
            programmes_list = []
            for programme in programmes:
                programmes_list.append(
                    {
                        "id": programme.id,
                        "name": programme.name,
                        "abbreviation": programme.abbreviation,
                    }
                )
            logger.info(f"Retrieved programmes list.{programmes_list}")
            return jsonify(programmes_list), 200
        else:
            logger.warning("No programmes found.")
            abort(404, "No programmes found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


#!IS THIS NECESSARY?
@programme_bp.route("/programmes/<int:programme_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_programme_by_id(programme_id):
    try:
        programme = db.session.query(Programme).filter_by(id=programme_id).first()
        if programme:
            logger.info(f"Retrieved programme.{programme}")
            return {
                "id": programme.id,
                "name": programme.name,
                "abbreviation": programme.abbreviation,
            }, 200
        else:
            logger.warning(f"No programme with ID={programme_id} found.")
            return abort(404, f"No programme with ID={programme_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@programme_bp.route("/programmes/<int:programme_id>", methods=["PUT"])
@login_required
@limiter.limit("50 per minute")
def update_programme(programme_id):
    if current_user.user_type == 0:
        try:
            new_name = clean(request.form.get("new_name"))
            new_abbreviation = clean(request.form.get("new_abbreviation"))
            affected_rows = (
                db.session.query(Programme)
                .filter_by(id=programme_id)
                .update({"name": new_name, "abbreviation": new_abbreviation})
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Programme with ID={programme_id} updated")
                return {"response": f"Programme with ID={programme_id} updated"}, 200
            else:
                logger.warning(f"No programme with ID={programme_id} to update")
                return abort(404, f"No programme with ID={programme_id} to update")
        except (ValueError, TypeError) as e:
            logger.error(f"An error has occured: request parameters not ok.\n{e}")
            abort(400, f"An error has occured: request parameters not ok.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@programme_bp.route("/programmes/<int:programme_id>", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def delete_programme(programme_id):
    if current_user.user_type == 0:
        try:
            affected_rows = (
                db.session.query(Programme).filter_by(id=programme_id).delete()
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Programme with ID={programme_id} deleted")
                return {"response": f"Programme with ID={programme_id} deleted"}, 200
            else:
                logger.warning(f"No programme with ID={programme_id} to delete")
                return abort(404, f"No programme with ID={programme_id} to delete")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")
