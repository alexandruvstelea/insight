from flask import Blueprint, jsonify, request
from models.rooms import Room
from __init__ import db
from sqlalchemy import exc
from sqlalchemy.orm import Session

room_bp = Blueprint("rooms", __name__)


@room_bp.route("/rooms", methods=["POST"])
def create_room():
    name = request.form["name"]
    new_room = Room(name)
    try:
        db.session.add(new_room)
        db.session.commit()
        return {"response": "New room added to database"}
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@room_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = db.session.query(Room).all()
    rooms_list = []
    for room in rooms:
        rooms_list.append({"id": room.id, "name": room.name})
    return jsonify(rooms_list)


@room_bp.route("/rooms/<int:room_id>", methods=["GET"])
def get_room_by_id(room_id):
    room = db.session.query(Room).filter_by(id=room_id).first()
    if room:
        return {"id": room.id, "name": room.name}
    else:
        return {"response": f"No room with ID={room_id} found."}


@room_bp.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    new_room = request.form["new_room"]
    try:
        affected_rows = (
            db.session.query(Room).filter_by(id=room_id).update({"name": new_room})
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Room with ID={room_id} updated"}
    else:
        return {"response": f"No room with ID={room_id} to update"}


@room_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    affected_rows = db.session.query(Room).filter_by(id=room_id).delete()
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Room with ID={room_id} deleted"}
    else:
        return {"response": f"No room with ID={room_id} to delete"}
