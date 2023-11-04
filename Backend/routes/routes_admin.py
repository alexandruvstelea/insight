from flask import Flask, jsonify, request, abort, Blueprint
from flask_jwt_extended import create_access_token
from bleach import clean
from dotenv import load_dotenv
from os import getenv

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["POST"])
def login():
    try:
        username = clean(request.form["username"])
        password = clean(request.form["password"])
    except KeyError as e:
        abort(400, f"An error has occured: missing key in request parameters.\n {e}")

    if username != getenv("ADMIN_USER") or password != getenv("ADMIN_PASSWORD"):
        return jsonify({"response": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
