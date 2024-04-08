from flask_login import current_user, login_required
from flask import Blueprint, abort
from __init__ import db, limiter
from models.codes import Code
from sqlalchemy import exc
import logging

logger = logging.getLogger(__name__)
code_bp = Blueprint("code", __name__)


@code_bp.route("/code/<int:room_id>",methods=["GET"])
@limiter.limit("50 per minute")
@login_required
def get_code(room_id):
    if current_user.user_type == 0:
        try:
            code = db.session.query(Code).filter(Code.room_id == room_id).first()
            if code:
                 logger.info(f"Code retrieved from database. {code}")
                 return {"code":code.code}
            else:
                logger.info(f"Could'nt find code.")
                abort(404, "Couldn't find code.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while retrieving code.\n{e}")
            abort(500, f"An error has occured while retrieving code.")
    abort(401, "Account not authorized to perform this action.")