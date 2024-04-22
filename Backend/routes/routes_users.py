from routes.helpers import (
    send_password_email,
    send_registration_email,
    check_email,
    check_password,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, abort, request, session
from __init__ import db, limiter, login_manager
from models.programmes import Programme
from dotenv import load_dotenv
from models.users import User
from random import randint
from sqlalchemy import exc
from bleach import clean
import logging
import os

logger = logging.getLogger(__name__)
user_bp = Blueprint("users", __name__)
load_dotenv(os.path.normpath("../.env"))


@user_bp.route("/users", methods=["GET"])
@login_required
def get_users():
    if current_user.user_type == 0:
        try:
            users = db.session.query(User).all()
            if users:
                users_list = []
                for user in users:
                    users_list.append(
                        {
                            "id": user.id,
                            "email": user.email,
                            "password": user.password,
                            "programme_id": user.programme_id,
                            "user_type": user.user_type,
                            "registration_code": user.registration_code,
                            "active": user.active,
                        }
                    )
                logger.info(f"Retrieved users list.{users_list}")
                return jsonify(users_list), 200
            else:
                logger.warning("No users found.")
                abort(404, "No users found.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@user_bp.route("/register", methods=["POST"])
@limiter.limit("1 per minute")
def register():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        programme_id = int(clean(request.form.get("programme_id")))
        if not check_email(email):
            abort(400, "The provided email is not institutional.")
        if not check_password(password):
            abort(400, "The provided password is too short.")
        code = randint(100000, 999999)
        hashed_password = generate_password_hash(password)
        existing_programme = (
            db.session.query(Programme).filter_by(id=programme_id).first()
        )
        if not existing_programme:
            abort(400, "Invalid programme ID.")
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            logger.warning("User already exists.")
            abort(400, "User already exists.")
        new_user = User(
            email=email,
            password=hashed_password,
            programme_id=programme_id,
            registration_code=code,
        )
        db.session.add(new_user)
        db.session.commit()
        send_registration_email(code, email)
        return {"message": "Registration successful!"}, 201
    except (ValueError, TypeError) as e:
        logger.error(f"An error has occured: request parameters not ok.\n{e}")
        abort(400, f"An error has occured: request parameters not ok.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route(f"/users/<int:user_id>", methods=["DELETE"])
@limiter.limit("50 per minute")
@login_required
def delete_user(user_id):
    if current_user.user_type == 0:
        try:
            affected_rows = db.session.query(User).filter_by(id=user_id).delete()
            if affected_rows > 0:
                db.session.commit()
                logger.info(f"User with ID={user_id} deleted")
                return {"response": f"User with ID={user_id} deleted"}, 200
            else:
                logger.warning(f"No user with ID={user_id} to delete")
                return abort(404, f"No user with ID={user_id} to delete")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while interacting with the database.\n{e}")
            abort(500, f"An error occurred while interacting with the database.")
    abort(401, "Account not authorized to perform this action.")


@user_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.active == 1:
            login_user(user)
            return {"message": "Login successful!"}, 200
        elif user and check_password_hash(user.password, password) and user.active == 0:
            return {"message": "Account not activated."}
        abort(401, "Invalid username or password!")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route("/request-reset", methods=["POST"])
@limiter.limit("1 per minute")
def request_reset_password():
    try:
        email = clean(request.form.get("email"))
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.active == 1:
            code = randint(100000, 999999)
            affected_rows = (
                db.session.query(User)
                .filter_by(email=email)
                .update({"registration_code": code})
            )
            if affected_rows > 0:
                db.session.commit()
            send_password_email(code, email)
            return {"message": "Password reset code sent."}
        else:
            if not user:
                abort(400, f"No user with email {email} found.")
            if user.active == 0:
                abort(400, f"User with email {email} not active.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route("/reset", methods=["POST"])
@limiter.limit("1 per minute")
def reset_password():
    try:
        email = clean(request.form.get("email"))
        code = int(clean(request.form.get("code")))
        new_password = clean(request.form.get(f"new_password"))
        if not check_password(new_password):
            abort(400, "The provided password is too short.")
        hashed_password = generate_password_hash(new_password)
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.active == 1 and user.registration_code == code:
            affected_rows = (
                db.session.query(User)
                .filter_by(email=email)
                .update({"password": hashed_password})
            )
            if affected_rows > 0:
                db.session.commit()
            send_password_email(code, email)
            return {"message": "Password reset."}
        else:
            if not user:
                abort(400, f"No user with email {email} found.")
            if user.active == 0:
                abort(400, f"User with email {email} not active.")
            if user.registration_code != code:
                abort(400, "The provided code is not valid.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route("/resend", methods=["PUT"])
@limiter.limit("1 per minute")
def resend_activation_code():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.active == 0:
            code = randint(100000, 999999)
            affected_rows = (
                db.session.query(User)
                .filter_by(email=email)
                .update({"registration_code": code})
            )
            if affected_rows > 0:
                db.session.commit()
            send_registration_email(code, email)
            return {"message": "New registration code sent."}
        else:
            if not user:
                abort(400, f"No user with email {email} found.")
            if user.active == 1:
                abort(400, f"User with email {email} already active.")
            if not check_password_hash(user.password, password):
                abort(400, "Invalid current password.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route("/activate", methods=["POST"])
@limiter.limit("10 per minute")
def activate_account():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        code = int(clean(request.form.get("code")))
        user = db.session.query(User).filter_by(email=email).first()
        if (
            user
            and check_password_hash(user.password, password)
            and user.active == 0
            and user.registration_code == code
        ):
            affected_rows = (
                db.session.query(User).filter_by(email=email).update({"active": 1})
            )
            if affected_rows > 0:
                db.session.commit()
            return {"message": "Account activated."}
        else:
            if not user:
                abort(400, f"No user with email {email} found.")
            if user.active == 1:
                abort(400, f"User with email {email} already active.")
            if not check_password_hash(user.password, password):
                abort(400, "Invalid password.")
            if user.registration_code != code:
                abort(400, "The provided code is not valid.")
    except (ValueError, TypeError) as e:
        logger.error(f"An error has occured: request parameters not ok.\n{e}")
        abort(400, f"An error has occured: request parameters not ok.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while interacting with the database.\n{e}")
        abort(500, f"An error occurred while interacting with the database.")


@user_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out successfully!"}, 200


@user_bp.route("/check-login", methods=["GET"])
def check_login_status():
    if current_user.is_authenticated:
        return {
            "logged_in": True,
            "user": current_user.email,
            "type": current_user.user_type,
        }, 200
    else:
        return {"logged_in": False}, 200


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
