from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, abort
from __init__ import db, limiter, login_manager
from models.programmes import Programme
from dotenv import load_dotenv
from models.users import User
from random import randint
from sqlalchemy import exc
from bleach import clean
import logging
import yagmail
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
            users_list = []
            if users:
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
            logger.error(f"An error has occured while retrieving objects.\n {e}")
            abort(500, f"An error has occured while retrieving objects.")
    abort(401, "Not authorized")


@user_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        programme_id = int(clean(request.form.get("programme_id")))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    if not check_email_password(email, password):
        abort(400, "Not institutional email or password too short.")
    code = randint(100000, 999999)
    hashed_password = generate_password_hash(password)
    try:
        with db.session.begin():
            existing_programme = (
                db.session.query(Programme).filter_by(id=programme_id).first()
            )
            if not existing_programme:
                abort(400, "Invalid programme ID.")
            existing_user = db.session.query(User).filter_by(email=email).first()
            if existing_user:
                abort(400, "User already exists.")
            new_user = User(
                email=email,
                password=hashed_password,
                programme_id=programme_id,
                registration_code=code,
            )
            db.session.add(new_user)
        send_registration_email(code, email)
        return {"message": "Registration successful!"}, 201
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while registering the user.\n {e}")
        return abort(500, f"An error has occured while registering the user.")


@user_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    try:
        with db.session.begin():
            user = db.session.query(User).filter_by(email=email).first()
            if (
                user
                and check_password_hash(user.password, password)
                and user.active == 1
            ):
                login_user(user)
                return {"message": "Login successful!"}, 200
            elif (
                user
                and check_password_hash(user.password, password)
                and user.active == 0
            ):
                return {"message": "Account not activated."}
            abort(401, "Invalid username or password!")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while authenticating the user.\n {e}")
        return abort(500, f"An error has occured while authenticating the user.")


@user_bp.route("/request-reset", methods=["GET"])
@limiter.limit("10 per minute")
def request_reset_password():
    try:
        email = clean(request.form.get("email"))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    try:
        with db.session.begin():
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
                abort(400, "Invalid credentials or account already inactive.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while sending email.\n {e}")
        return abort(500, f"An error has occured while sending email.")


@user_bp.route("/reset", methods=["GET"])
@limiter.limit("10 per minute")
def reset_password():
    try:
        email = clean(request.form.get("email"))
        code = int(clean(request.form.get("code")))
        new_password = clean(request.form.get(f"new_password"))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    if not check_email_password(email, new_password):
        abort(400, "Not institutional email or password too short.")
    hashed_password = generate_password_hash(new_password)
    try:
        with db.session.begin():
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
                abort(400, "Invalid credentials.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while reseting password.\n {e}")
        return abort(500, f"An error has occured while reseting password.")


@user_bp.route("/resend", methods=["PUT"])
@limiter.limit("10 per minute")
def resend_activation_code():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    try:
        with db.session.begin():
            user = db.session.query(User).filter_by(email=email).first()
            if (
                user
                and check_password_hash(user.password, password)
                and user.active == 0
            ):
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
                abort(400, "Invalid credentials or account already active.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while resending email.\n {e}")
        return abort(500, f"An error has occured while resending email.")


@user_bp.route("/activate", methods=["POST"])
@limiter.limit("10 per minute")
def activate_account():
    try:
        email = clean(request.form.get("email"))
        password = clean(request.form.get("password"))
        code = int(clean(request.form.get("code")))
    except KeyError as e:
        logger.error(f"An error has occured: missing key in request parameters.\n {e}")
        abort(400, f"An error has occured: missing key in request parameters.")
    try:
        with db.session.begin():
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
                abort(400, "Invalid credentials or account already active.")
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while activating account.\n {e}")
        return abort(500, f"An error has occured while activating account.")


@user_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out successfully!"}, 200


@user_bp.route("/check-login", methods=["GET"])
def check_login_status():
    if current_user.is_authenticated:
        return {"logged_in": True, "user": current_user.email}, 200
    else:
        return {"logged_in": False}, 200


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def send_registration_email(code: int, email: str):
    try:
        EMAIL = os.getenv("EMAIL")
        PASSWORD = os.getenv("PASSWORD")
        yag = yagmail.SMTP(EMAIL, PASSWORD)
        contents = [
            f"""
            <html>
                <body>
                    <p>Salut!</p>
                    <p>Mai jos vei găsi codul unic necesar pentru a-ți activa contul pe FeedbackIESC.</p>
                    <p><b>Codul tău: {code}</b></p>
                    <p>Te rugăm să introduci acest cod în câmpul corespunzător pe site pentru a continua.</p>
                    <p>Dacă nu ai solicitat acest cod, te rugăm să ignori acest e-mail sau să ne contactezi pentru asistență.</p>
                    <p>O zi excelentă,</p>
                    <p>Echipa Feedback IESC</p>
                </body>
            </html>
            """
        ]
        yag.send(email, "Codul tău Feedback IESC pentru activarea contului", contents)
        # logger.info(f"Email sent to {email} with code {code}.")
    except Exception as e:
        logger.error(
            f"An error has occured while sending an email to {email}.\n {str(e)}"
        )
        return e


def send_password_email(code: int, email: str):
    try:
        EMAIL = os.getenv("EMAIL")
        PASSWORD = os.getenv("PASSWORD")
        yag = yagmail.SMTP(EMAIL, PASSWORD)
        contents = [
            f"""
            <html>
                <body>
                    <p>Salut!</p>
                    <p>Mai jos vei găsi codul unic necesar pentru a-ți schimba parola contului FeedbackIESC.</p>
                    <p><b>Codul tău: {code}</b></p>
                    <p>Te rugăm să introduci acest cod în câmpul corespunzător pe site pentru a continua.</p>
                    <p>Dacă nu ai solicitat acest cod, te rugăm să ignori acest e-mail sau să ne contactezi pentru asistență.</p>
                    <p>O zi excelentă,</p>
                    <p>Echipa Feedback IESC</p>
                </body>
            </html>
            """
        ]
        yag.send(email, "Codul tău Feedback IESC pentru resetarea parolei", contents)
        # logger.info(f"Email sent to {email} with code {code}.")
    except Exception as e:
        logger.error(
            f"An error has occured while sending an email to {email}.\n {str(e)}"
        )
        return e


def check_email_password(email: str, password: str):
    if len(password) > 7 and email.endswith("@student.unitbv.ro"):
        return True
    return False
