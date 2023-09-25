from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from rooms import Room
from courses import Course
from professors import Professor
from programmes_subjects import ProgrammesSubjects
from programmes import Programme
from subjects import Subject
from ratings import Rating
from database import session, Base, engine
from sqlalchemy import exc, and_, select, func


app = Flask(__name__)


@app.route("/rooms", methods=["POST"])
def create_room():
    name = request.form["name"]
    new_room = Room(name)
    try:
        session.add(new_room)
        session.commit()
        return {"response": "New room added to database"}
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = session.query(Room).all()
    rooms_list = []
    for room in rooms:
        rooms_list.append({"id": room.id, "name": room.name})
    return jsonify(rooms_list)


@app.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    new_room = request.form["new_room"]
    try:
        affected_rows = (
            session.query(Room).filter_by(id=room_id).update({"name": new_room})
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Room with ID={room_id} updated"}
    else:
        return {"response": f"No room with ID={room_id} to update"}


@app.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    affected_rows = session.query(Room).filter_by(id=room_id).delete()
    if affected_rows > 0:
        session.commit()
        return {"response": f"Room with ID={room_id} deleted"}
    else:
        return {"response": f"No room with ID={room_id} to delete"}


@app.route("/professors", methods=["POST"])
def create_professor():
    name = request.form["name"]
    surname = request.form["surname"]
    title = request.form["title"]
    new_professor = Professor(name, surname, title)
    try:
        session.add(new_professor)
        session.commit()
        return {"response": "New professor added to database"}
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/professors", methods=["GET"])
def get_professors():
    professors = session.query(Professor).all()
    professors_list = []
    for professor in professors:
        professors_list.append(
            {
                "id": professor.id,
                "name": professor.name,
                "surname": professor.surname,
                "title": professor.title,
            }
        )
    return jsonify(professors_list)


@app.route("/professors/<int:professor_id>", methods=["PUT"])
def update_professor(professor_id):
    new_name = request.form["new_name"]
    new_surname = request.form["new_surname"]
    new_title = request.form["new_title"]
    try:
        affected_rows = (
            session.query(Professor)
            .filter_by(id=professor_id)
            .update(
                {
                    "name": new_name,
                    "surname": new_surname,
                    "title": new_title,
                }
            )
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Professor with ID={professor_id} updated"}
    else:
        return {"response": f"No professor with ID={professor_id} to update"}


@app.route("/professors/<int:professor_id>", methods=["DELETE"])
def delete_professor(professor_id):
    affected_rows = session.query(Professor).filter_by(id=professor_id).delete()
    if affected_rows > 0:
        session.commit()
        return {"response": f"Professor with ID={professor_id} deleted"}
    else:
        return {"response": f"No professor with ID={professor_id} to delete"}


@app.route("/programmes", methods=["POST"])
def create_programme():
    name = request.form["name"]
    abbreviation = request.form["abbreviation"]
    new_programme = Programme(name, abbreviation)
    try:
        session.add(new_programme)
        session.commit()
        return {"response": "New programme added to database"}
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/programmes", methods=["GET"])
def get_programmes():
    programmes = session.query(Programme).all()
    programmes_list = []
    for programme in programmes:
        programmes_list.append(
            {
                "id": programme.id,
                "name": programme.name,
                "abbreviation": programme.abbreviation,
            }
        )
    return jsonify(programmes_list)


@app.route("/programmes/<int:programme_id>", methods=["PUT"])
def update_programme(programme_id):
    new_name = request.form["new_name"]
    new_abbreviation = request.form["new_abbreviation"]
    try:
        affected_rows = (
            session.query(Programme)
            .filter_by(id=programme_id)
            .update(
                {
                    "name": new_name,
                    "abbreviation": new_abbreviation,
                }
            )
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Programme with ID={programme_id} updated"}
    else:
        return {"response": f"No programme with ID={programme_id} to update"}


@app.route("/programmes/<int:programme_id>", methods=["DELETE"])
def delete_programmes(programme_id):
    affected_rows = session.query(Programme).filter_by(id=programme_id).delete()
    if affected_rows > 0:
        session.commit()
        return {"response": f"Programme with ID={programme_id} deleted"}
    else:
        return {"response": f"No programme with ID={programme_id} to delete"}


@app.route("/subjects", methods=["POST"])
def create_subject():
    name = request.form["name"]
    abbreviation = request.form["abbreviation"]
    professor_id = request.form["professor_id"]
    new_subject = Subject(name, abbreviation, professor_id)
    try:
        session.add(new_subject)
        session.commit()
        return {"response": "New subject added to database"}
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/subjects", methods=["GET"])
def get_subject():
    subjects = session.query(Subject).all()
    subjects_list = []
    for subject in subjects:
        subjects_list.append(
            {
                "id": subject.id,
                "name": subject.name,
                "abbreviation": subject.abbreviation,
                "professor_id": subject.professor_id,
            }
        )
    return jsonify(subjects_list)


@app.route("/subjects/<int:subject_id>", methods=["PUT"])
def update_subject(subject_id):
    new_name = request.form["new_name"]
    new_abbreviation = request.form["new_abbreviation"]
    new_professor_id = request.form["new_professor_id"]
    try:
        affected_rows = (
            session.query(Subject)
            .filter_by(id=subject_id)
            .update(
                {
                    "name": new_name,
                    "abbreviation": new_abbreviation,
                    "professor_id": new_professor_id,
                }
            )
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Subject with ID={subject_id} updated"}
    else:
        return {"response": f"No subject with ID={subject_id} to update"}


@app.route("/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subjects(subject_id):
    affected_rows = session.query(Subject).filter_by(id=subject_id).delete()
    if affected_rows > 0:
        session.commit()
        return {"response": f"Subject with ID={subject_id} deleted"}
    else:
        return {"response": f"No subject with ID={subject_id} to delete"}


@app.route("/programmesubjects", methods=["POST"])
def create_programme_subject():
    programme_id = request.form["programme_id"]
    subject_id = request.form["subject_id"]
    new_relation = ProgrammesSubjects(programme_id, subject_id)
    try:
        session.add(new_relation)
        session.commit()
        return {"response": "New relation added to database"}
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/programmesubjects", methods=["GET"])
def get_programmes_subjects():
    relations = session.query(ProgrammesSubjects).all()
    relations_list = []
    for relation in relations:
        relations_list.append(
            {
                "programme_id": relation.programme_id,
                "subject_id": relation.subject_id,
            }
        )
    return jsonify(relations_list)


@app.route("/programmesubjects/<int:programme_id>/<int:subject_id>", methods=["PUT"])
def update_programmes_subjects(programme_id, subject_id):
    new_programme_id = request.form["new_programme_id"]
    new_subject_id = request.form["new_subject_id"]
    try:
        affected_rows = (
            session.query(ProgrammesSubjects)
            .filter(
                and_(
                    ProgrammesSubjects.programme_id == programme_id,
                    ProgrammesSubjects.subject_id == subject_id,
                )
            )
            .update(
                {
                    "programme_id": new_programme_id,
                    "subject_id": new_subject_id,
                }
            )
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Relation [{programme_id,subject_id}] updated."}
    else:
        return {"response": f"No relation [{programme_id,subject_id}] to update."}


@app.route("/programmesubjects/<int:programme_id>/<int:subject_id>", methods=["DELETE"])
def delete_programmes_subjects(programme_id, subject_id):
    affected_rows = (
        session.query(ProgrammesSubjects)
        .filter(
            and_(
                ProgrammesSubjects.programme_id == programme_id,
                ProgrammesSubjects.subject_id == subject_id,
            )
        )
        .delete()
    )
    if affected_rows > 0:
        session.commit()
        return {"response": f"Relation [{programme_id,subject_id}] deleted."}
    else:
        return {"response": f"No relation [{programme_id,subject_id}] to delete."}


@app.route("/courses", methods=["POST"])
def create_course():
    subject_id = request.form["subject_id"]
    type = request.form["type"]
    room_id = request.form["room_id"]
    day = request.form["day"]
    week_type = request.form["week_type"]
    start = request.form["start"]
    end = request.form["end"]
    start_end = [start, end]
    try:
        new_course = Course(subject_id, type, room_id, day, week_type, start_end)
        session.add(new_course)
        session.commit()
        return {"response": "New course added to database"}
    except:
        session.rollback()
        return {"response": "An error has occured"}, 404


@app.route("/courses", methods=["GET"])
def get_courses():
    courses = session.query(Course).all()
    courses_list = []
    for course in courses:
        courses_list.append(
            {
                "id": course.id,
                "subject_id": course.subject_id,
                "type": course.type,
                "room_id": course.room_id,
                "day": course.day,
                "week_type": course.week_type,
                "start": course.start_end[0].strftime("%H:%M"),
                "end": course.start_end[1].strftime("%H:%M"),
            }
        )
    return jsonify(courses_list)


@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    new_subject_id = request.form["new_subject_id"]
    new_type = request.form["new_type"]
    new_room_id = request.form["new_room_id"]
    new_day = request.form["new_day"]
    new_week_type = request.form["new_week_type"]
    new_start = request.form["new_start"]
    new_end = request.form["new_end"]
    new_start_end = [new_start, new_end]
    try:
        affected_rows = (
            session.query(Course)
            .filter_by(id=course_id)
            .update(
                {
                    "subject_id": new_subject_id,
                    "type": new_type,
                    "room_id": new_room_id,
                    "day": new_day,
                    "week_type": new_week_type,
                    "start_end": new_start_end,
                }
            )
        )
    except exc.IntegrityError:
        session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        session.commit()
        return {"response": f"Course with ID={course_id} updated."}
    else:
        return {"response": f"No course with ID={course_id} to update."}


@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    affected_rows = session.query(Course).filter_by(id=course_id).delete()
    if affected_rows > 0:
        session.commit()
        return {"response": f"Course with ID={course_id} deleted."}
    else:
        return {"response": f"No course with ID={course_id} to delete."}


@app.route("/rating", methods=["POST"])
def insert_rating():
    data = request.get_json()
    date_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
    rating = int(data["rating"])
    room_id = int(data["room"])
    #subject_id = get_current_subject(date_time, room_id)
    subject_id = 2
    #try:
    new_rating = Rating(rating, subject_id, room_id, date_time)
    session.add(new_rating)
    session.commit()
    return {"response": "New rating added to database"}
    #except Exception:
    #    session.rollback()
    #    return {"response": "An error has occured"}, 404


@app.route("/rating/<int:subject_id>", methods=["GET"])
def get_average_rating(subject_id):
    average_rating = select(func.avg(Rating)).where(Rating.subject_id == subject_id)
    result = session.execute(average_rating).scalar()
    return {"response": result}

@app.route("/current",methods=["GET"])
def get_current_course():
    return {"id":2,"name":"Inteligenta Artificiala","abbreviation":"IA"}

if __name__ == "__main__":
    CORS(app)
    app.run(host='0.0.0.0',debug=True)
