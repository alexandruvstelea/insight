from flask import Blueprint, jsonify, request, abort
from models.rooms import Room
from __init__ import db, limiter
from sqlalchemy import exc
from bleach import clean

room_bp = Blueprint("rooms", __name__)


@room_bp.route("/rooms", methods=["POST"])
@limiter.limit("50 per minute")
def create_room():
    try:
        name = clean(request.form["name"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    new_room = Room(name)
    try:
        with db.session.begin():
            db.session.add(new_room)
            db.session.commit()
            return {"response": "New room added to database"}, 200
    except exc.SQLAlchemyError as e:
        return abort(
            500, f"An error has occured while adding object to the database.\n {str(e)}"
        )


@room_bp.route("/rooms", methods=["GET"])
@limiter.limit("50 per minute")
def get_rooms():
    try:
        rooms = db.session.query(Room).all()
        rooms_list = []
        if rooms:
            for room in rooms:
                rooms_list.append({"id": room.id, "name": room.name})
            return jsonify(rooms_list), 200
        else:
            abort(404, "No rooms found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving objects.\n {str(e)}")


@room_bp.route("/rooms/<int:room_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_room_by_id(room_id):
    try:
        room = db.session.query(Room).filter_by(id=room_id).first()
        if room:
            return {"id": room.id, "name": room.name}, 200
        else:
            return abort(404, f"No room with ID={room_id} found.")
    except exc.SQLAlchemyError as e:
        abort(500, f"An error has occured while retrieving objects.\n {str(e)}")


@room_bp.route("/rooms/<int:room_id>", methods=["PUT"])
@limiter.limit("50 per minute")
def update_room(room_id):
    try:
        new_room = clean(request.form["new_room"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")
    try:
        with db.session.begin():
            affected_rows = (
                db.session.query(Room).filter_by(id=room_id).update({"name": new_room})
            )
            if affected_rows > 0:
                db.session.commit()
                return {"response": f"Room with ID={room_id} updated"}, 200
            else:
                return abort(404, f"No room with ID={room_id} to update")
    except exc.SQLAlchemyError as e:
        return abort(500, f"An error has occured while updating object.\n {str(e)}")


@room_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
@limiter.limit("50 per minute")
def delete_room(room_id):
    try:
        affected_rows = db.session.query(Room).filter_by(id=room_id).delete()
        if affected_rows > 0:
            db.session.commit()
            return {"response": f"Room with ID={room_id} deleted"}, 200
        else:
            return abort(404, f"No room with ID={room_id} to delete")
    except exc.SQLAlchemyError as e:
        return abort(500, f"An error has occured while updating object.\n {str(e)}")
