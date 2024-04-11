from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from routes.helpers import verify_code, last_three_digits
from models.tablets import Tablet
from __init__ import db, limiter
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import exc
from bleach import clean
import logging
import os

logger = logging.getLogger(__name__)
tablet_bp = Blueprint("tablets", __name__)
load_dotenv(os.path.normpath("../.env"))


@tablet_bp.route("/tablets", methods=["GET"])
@login_required
@limiter.limit("50 per minute")
def get_rooms():
    if current_user.user_type == 0:
        try:
            tablets = db.session.query(Tablet).all()
            tablets_list = []
            if tablets:
                for tablet in tablets:
                    tablets_list.append(
                        {
                            "id": tablet.id,
                            "room_id": tablet.room_id,
                            "last_ping": tablet.last_ping,
                        }
                    )
                logger.info(f"Retrieved tablets list.{tablets_list}")
                return jsonify(tablets_list), 200
            else:
                logger.warning("No tablets found.")
                abort(404, "No tablets found.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while retrieving tablets.\n{e}")
            abort(500, f"An error has occured while retrieving tablets.")
    abort(401, "Account not authorized to perform this action.")


@tablet_bp.route("/ping/<int:room_id>", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def ping(room_id):
    if current_user.user_type == 0:
        try:
            affected_rows = (
                db.session.query(Tablet)
                .filter_by(room_id=room_id)
                .update({"last_ping": datetime.now()})
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Pinged tablet for room with id={room_id}.")
                return {"response": "Pinged."}, 200
            else:
                logger.info(
                    f"Did not find existing tablet for room with id={room_id}. Creating one."
                )
                new_tablet = Tablet(room_id, datetime.now())
                db.session.add(new_tablet)
                db.session.commit()
                logger.info(
                    f"New tablet generated and pinged for room with id={room_id}."
                )
                return {"response": "Created and pinged."}, 200
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while pinging.\n{e}")
            abort(500, f"An error has occured while pinging.")
    abort(401, "Account not authorized to perform this action.")
