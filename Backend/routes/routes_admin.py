from flask import Flask, jsonify, request, abort, Blueprint
from flask_jwt_extended import create_access_token
from bleach import clean
from dotenv import load_dotenv
from os import getenv
from __init__ import limiter
import logging

logger = logging.getLogger(__name__)
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["POST"])
@limiter.limit("50 per minute")
def login():
    try:
        username = clean(request.form["username"])
        password = clean(request.form["password"])
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")

    if username != getenv("ADMIN_USER") or password != getenv("ADMIN_PASSWORD"):
        logger.warning("Bad username or password.")
        return jsonify({"response": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    logger.info("Acces token generated and sent.")
    return jsonify(access_token=access_token), 200
