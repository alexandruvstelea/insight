from sqlalchemy import exc, and_
from models.rooms import Room
from models.professors import Professor
from models.programmes import Programme
from models.subjects import Subject
from models.courses import Course
from models.programmes_subjects import ProgrammesSubjects
from database import session, Base, engine

Base.metadata.create_all(engine)


def create_room(room: Room):
    try:
        session.add(room)
        session.commit()
        print("Room added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_room(room_id: int):
    affected_rows = session.query(Room).filter_by(id=room_id).delete()
    if affected_rows > 0:
        session.commit()
        print(f"Room with id {room_id} deleted.")
    else:
        print(f"No room with id {room_id} to delete.")


def update_room(room_id: int, new_room: Room):
    affected_rows = (
        session.query(Room).filter_by(id=room_id).update({"name": new_room.name})
    )
    if affected_rows > 0:
        session.commit()
        print(f"Room with id {room_id} updated.")
    else:
        print(f"No room with id {room_id} to update.")


def display_rooms():
    rooms = session.query(Room).all()
    if rooms:
        for room in rooms:
            print(room)
    else:
        print("No rooms to display.")


def create_professor(professor: Professor):
    try:
        session.add(professor)
        session.commit()
        print("Professor added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_professor(professor_id: int):
    affected_rows = session.query(Professor).filter_by(id=professor_id).delete()
    if affected_rows > 0:
        session.commit()
        print(f"Professor with id {professor_id} deleted.")
    else:
        print(f"No professor with id {professor_id} to delete.")


def update_professor(professor_id: int, new_professor: Professor):
    affected_rows = (
        session.query(Professor)
        .filter_by(id=professor_id)
        .update(
            {
                "name": new_professor.name,
                "surname": new_professor.surname,
                "title": new_professor.title,
            }
        )
    )
    if affected_rows > 0:
        session.commit()
        print(f"Professor with id {professor_id} updated.")
    else:
        print(f"No professor with id {professor_id} to update.")


def display_professors():
    professors = session.query(Professor).all()
    if professors:
        for professor in professors:
            print(professor)
    else:
        print("No professors to display.")


def create_programme(programme: Programme):
    try:
        session.add(programme)
        session.commit()
        print("Programme added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_programme(programme_id: int):
    affected_rows = session.query(Programme).filter_by(id=programme_id).delete()
    if affected_rows > 0:
        session.commit()
        print(f"Programme with id {programme_id} deleted.")
    else:
        print(f"No programme with id {programme_id} to delete.")


def update_programme(programme_id: int, new_programme: Programme):
    affected_rows = (
        session.query(Programme)
        .filter_by(id=programme_id)
        .update(
            {
                "name": new_programme.name,
                "abbreviation": new_programme.abbreviation,
            }
        )
    )
    if affected_rows > 0:
        session.commit()
        print(f"Programme with id {programme_id} updated.")
    else:
        print(f"No programme with id {programme_id} to update.")


def display_programmes():
    programmes = session.query(Programme).all()
    if programmes:
        for programme in programmes:
            print(programme)
    else:
        print("No programmes to display.")


def create_subject(subject: Subject):
    try:
        session.add(subject)
        session.commit()
        print("Subject added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_subject(subject_id: int):
    affected_rows = session.query(Subject).filter_by(id=subject_id).delete()
    if affected_rows > 0:
        session.commit()
        print(f"Subject with id {subject_id} deleted.")
    else:
        print(f"No subject with id {subject_id} to delete.")


def update_subject(subject_id: int, new_subject: Subject):
    affected_rows = (
        session.query(Subject)
        .filter_by(id=subject_id)
        .update(
            {
                "name": new_subject.name,
                "abbreviation": new_subject.abbreviation,
                "professor_id": new_subject.professor_id,
            }
        )
    )
    if affected_rows > 0:
        session.commit()
        print(f"Subject with id {subject_id} updated.")
    else:
        print(f"No subject with id {subject_id} to update.")


def display_subjects():
    subjects = session.query(Subject).all()
    if subjects:
        for subject in subjects:
            print(subject)
    else:
        print("No subjects to display.")


def create_course(course: Course):
    try:
        session.add(course)
        session.commit()
        print("Course added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_course(course_id: int):
    affected_rows = session.query(Course).filter_by(id=course_id).delete()
    if affected_rows > 0:
        session.commit()
        print(f"Course with id {course_id} deleted.")
    else:
        print(f"No course with id {course_id} to delete.")


def update_course(course_id: int, new_course: Course):
    affected_rows = (
        session.query(Course)
        .filter_by(id=course_id)
        .update(
            {
                "subject_id": new_course.subject_id,
                "type": new_course.type,
                "room_id": new_course.room_id,
                "day": new_course.day,
                "week_type": new_course.week_type,
                "start_end": new_course.start_end,
            }
        )
    )
    if affected_rows > 0:
        session.commit()
        print(f"Course with id {course_id} updated.")
    else:
        print(f"No course with id {course_id} to update.")


def display_courses():
    courses = session.query(Course).all()
    if courses:
        for course in courses:
            print(course)
    else:
        print("No courses to display.")


def create_programme_subject(relation: ProgrammesSubjects):
    try:
        session.add(relation)
        session.commit()
        print("Relation added to database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"AN ERROR HAS OCCURED! \n {error}")


def delete_programme_subject(programme_id: int, subject_id: int):
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
        print(f"Relation [{programme_id,subject_id}] deleted.")
    else:
        print(f"No relation [{programme_id,subject_id}] to delete.")


def update_programme_subject(
    programme_id: int, subject_id: int, new_relation: ProgrammesSubjects
):
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
                "programme_id": new_relation.programme_id,
                "subject_id": new_relation.subject_id,
            }
        )
    )
    if affected_rows > 0:
        session.commit()
        print(f"Relation [{programme_id,subject_id}] updated.")
    else:
        print(f"No relation [{programme_id,subject_id}] to update.")


def display_programmes_subjects():
    relations = session.query(ProgrammesSubjects).all()
    if relations:
        count = 1
        for relation in relations:
            print(f"NR {count}->{relation}")
    else:
        print("No relations to display.")
