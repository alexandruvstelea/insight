from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from models.ratings import Rating
        from models.courses import Course
        from models.professors import Professor
        from models.programmes_subjects import ProgrammesSubjects
        from models.programmes import Programme
        from models.rooms import Room
        from models.subjects import Subject

        db.create_all()

        from routes.routes_courses import course_bp
        from routes.routes_professors import professor_bp
        from routes.routes_programmes import programme_bp
        from routes.routes_ratings import rating_bp
        from routes.routes_rooms import room_bp
        from routes.routes_subjects import subject_bp
        from routes.routes_programmes_subjects import programme_subjects_bp
        from routes.routes_graph import graph_bp

        app.register_blueprint(course_bp)
        app.register_blueprint(professor_bp)
        app.register_blueprint(programme_bp)
        app.register_blueprint(rating_bp)
        app.register_blueprint(room_bp)
        app.register_blueprint(subject_bp)
        app.register_blueprint(programme_subjects_bp)
        app.register_blueprint(graph_bp)

        return app
