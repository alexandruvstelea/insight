from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
import logging
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")
MONGO_USER = getenv("MONGODB_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = getenv("MONGODB_INITDB_ROOT_PASSWORD")
MONGO_HOST = getenv("MONGO_HOST")
MONGO_PORT = getenv("MONGO_PORT")

db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["50 per minute"],
    storage_uri=f"mongodb://localhost:27017",
    strategy="fixed-window",
)
login_manager = LoginManager()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    jwt = JWTManager(app)

    db.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models.ratings import Rating
        from models.courses import Course
        from models.professors import Professor
        from models.rooms import Room
        from models.subjects import Subject
        from models.weeks import Week
        from models.comments import Comment
        from models.programmes import Programme
        from models.users import User

        db.create_all()

        from routes.routes_courses import course_bp
        from routes.routes_professors import professor_bp
        from routes.routes_ratings import rating_bp
        from routes.routes_rooms import room_bp
        from routes.routes_subjects import subject_bp
        from routes.routes_weeks import weeks_bp
        from routes.routes_comments import comments_bp
        from routes.routes_archive import archive_bp
        from routes.routes_programmes import programme_bp
        from routes.routes_users import user_bp

        app.register_blueprint(course_bp)
        app.register_blueprint(professor_bp)
        app.register_blueprint(rating_bp)
        app.register_blueprint(room_bp)
        app.register_blueprint(subject_bp)
        app.register_blueprint(weeks_bp)
        app.register_blueprint(comments_bp)
        app.register_blueprint(archive_bp)
        app.register_blueprint(programme_bp)
        app.register_blueprint(user_bp)

        logging.basicConfig(
            filename="app.log",
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
        )
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())

        return app
