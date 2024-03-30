from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from models.rooms import Room
from __init__ import db, limiter
from sqlalchemy import exc
from bleach import clean
import logging

logger = logging.getLogger(__name__)
room_bp = Blueprint("rooms", __name__)


@room_bp.route("/rooms", methods=["POST"])
@login_required
@limiter.limit("50 per minute")
def create_room():
    if current_user.user_type == 0:
        try:
            name = clean(request.form["name"])
        except KeyError as e:
            logger.error(
                f"An error has occured: missing key in request parameters.\n{e}"
            )
            abort(400, f"An error has occured: missing key in request parameters.")
        new_room = Room(name)
        try:
            db.session.add(new_room)
            db.session.commit()
            logger.info("New room added to database")
            return {"response": "New room added to database"}, 200
        except exc.SQLAlchemyError as e:
            logger.error(
                f"An error has occured while adding room to the database.\n{e}"
            )
            return abort(
                500, f"An error has occured while adding room to the database."
            )
    abort(401, "Account not authorized to perform this action.")


@room_bp.route("/rooms", methods=["GET"])
@limiter.limit("50 per minute")
def get_rooms():
    try:
        rooms = db.session.query(Room).all()
        rooms_list = []
        if rooms:
            for room in rooms:
                rooms_list.append({"id": room.id, "name": room.name})
            logger.info(f"Retrieved rooms list.{rooms_list}")
            return jsonify(rooms_list), 200
        else:
            logger.warning("No rooms found.")
            abort(404, "No rooms found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving rooms.\n{e}")
        abort(500, f"An error has occured while retrieving rooms.")


@room_bp.route("/rooms/<int:room_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_room_by_id(room_id):
    try:
        room = db.session.query(Room).filter_by(id=room_id).first()
        if room:
            logger.info(f"Retrieved room.{room}")
            return {"id": room.id, "name": room.name}, 200
        else:
            logger.warning(f"No room with ID={room_id} found.")
            return abort(404, f"No room with ID={room_id} found.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving rooms.\n{e}")
        abort(500, f"An error has occured while retrieving rooms.")


@room_bp.route("/rooms/<int:room_id>", methods=["PUT"])
@login_required
@limiter.limit("50 per minute")
def update_room(room_id):
    if current_user.user_type == 0:
        try:
            new_room = clean(request.form["new_room"])
        except KeyError as e:
            logger.error(
                f"An error has occured: missing key in request parameters.\n{e}"
            )
            abort(400, f"An error has occured: missing key in request parameters.")
        try:
            affected_rows = (
                db.session.query(Room).filter_by(id=room_id).update({"name": new_room})
            )
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Room with ID={room_id} updated")
                return {"response": f"Room with ID={room_id} updated"}, 200
            else:
                logger.warning(f"No room with ID={room_id} to update")
                return abort(404, f"No room with ID={room_id} to update")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while updating room.\n{e}")
            return abort(500, f"An error has occured while updating room.")
    abort(401, "Account not authorized to perform this action.")


@room_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
@login_required
@limiter.limit("50 per minute")
def delete_room(room_id):
    if current_user.user_type == 0:
        try:
            affected_rows = db.session.query(Room).filter_by(id=room_id).delete()
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"Room with ID={room_id} deleted")
                return {"response": f"Room with ID={room_id} deleted"}, 200
            else:
                logger.warning(f"No room with ID={room_id} to delete")
                return abort(404, f"No room with ID={room_id} to delete")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error has occured while deleting room.\n{e}")
            return abort(500, f"An error has occured while deleting room.")
    abort(401, "Account not authorized to perform this action.")
