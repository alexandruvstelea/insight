from models.weeks import Week
from models.codes import Code
from sqlalchemy import exc
from __init__ import db
import logging
import yagmail
import os


logger = logging.getLogger(__name__)

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
    except Exception as error:
        logger.error(
            f"An error has occured while sending an email to {email}.\n {str(error)}"
        )
        return error


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
    except Exception as e:
        logger.error(f"An error has occured while sending an email to {email}.\n{e}")
        return e


def check_email(email: str):
    return email.endswith("@student.unitbv.ro")


def check_password(password: str):
    return len(password) > 7

def find_week_type(date_time):
    current_week = (
        db.session.query(Week)
        .filter(Week.start <= date_time, Week.end >= date_time)
        .first()
    )
    logger.info(f"{date_time}")
    if current_week:
        logger.info("Retrieved current week type.")
        return (
            [2, current_week.semester]
            if current_week.id % 2 == 0
            else [1, current_week.semester]
        )
    else:
        logger.error("Current week couldn't be determined.")
        return False
    
def verify_code(room_id:int, sent_code:int):
    try:
        code = db.session.query(Code).filter(Code.room_id == room_id).first()
        if code:
             if sent_code == code.code:
                return True
             else:
                 return False
    except exc.SQLAlchemyError as e:
        logger.error(f"An error has occured while retrieving code.\n{e}")