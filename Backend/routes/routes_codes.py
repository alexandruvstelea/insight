from flask_login import current_user, login_required
from routes.helpers import generate_voting_code
from flask import Blueprint, abort, request
from __init__ import db, limiter
from models.codes import Code
from sqlalchemy import exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
code_bp = Blueprint("code", __name__)


@code_bp.route("/code/<int:room_id>", methods=["GET"])
@limiter.limit("50 per minute")
@login_required
def get_code(room_id):
    if current_user.user_type == 0:
        try:
            code = db.session.query(Code).filter(Code.room_id == room_id).first()
            if code:
                logger.info(f"Code retrieved from database. {code}")
                return {"code": code.code}
            else:
                logger.info(f"Could'nt find code.")
                abort(404, "Couldn't find code.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while retrieving code.\n{e}")
            abort(500, f"An error has occured while retrieving code.")
    abort(401, "Account not authorized to perform this action.")


@code_bp.route("/code/<int:room_id>", methods=["POST"])
@limiter.limit("50 per minute")
@login_required
def regenerate_code(room_id):
    if current_user.user_type == 0:
        try:
            subject_id = int(clean(request.form["subject_id"]))
            code = generate_voting_code(subject_id)
            affected_rows = (
                db.session.query(Code).filter_by(room_id=room_id).update({"code": code})
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"New code generated for room with id={room_id}.")
                return {"response": "New code generated."}, 200
            else:
                logger.info(
                    f"Did not find existing code for room with id={room_id}. Creating one."
                )
                new_code = Code(code, room_id)
                db.session.add(new_code)
                db.session.commit()
                logger.info(f"New code generated for room with id={room_id}.")
                return {"response": "New code generated."}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while generating code.\n{e}")
            abort(500, f"An error has occured while generating code.")
        except KeyError as e:
            logger.error(
                f"An error has occured: missing key in request parameters.\n {e}"
            )
            abort(400, f"An error has occured: missing key in request parameters.")
        except (ValueError, TypeError) as e:
            logger.error("An error has occurred: subject id is not a number.")
            abort(400, f"An error has occurred: subject id is not a number.")
    abort(401, "Account not authorized to perform this action.")
