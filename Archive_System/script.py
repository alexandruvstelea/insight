import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
HOST = getenv("POSTGRES_HOST")
DB_NAME = getenv("POSTGRES_DB_NAME")
PORT = getenv("PORT")

conn = psycopg2.connect(
    dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
)


def create_table_copy(table_name):
    current_year = datetime.now().year
    new_table_name = f"{table_name}_{current_year-1}_{current_year}"

    cur = conn.cursor()

    try:
        cur.execute(
            f'CREATE TABLE "{new_table_name}" (LIKE "{table_name}" INCLUDING ALL)'
        )
        cur.execute(f'INSERT INTO "{new_table_name}" SELECT * FROM "{table_name}"')
        conn.commit()
        print(f"Table {table_name} copied as {new_table_name}")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    cur.close()
    return new_table_name


def update_foreign_keys(
    old_table_name, new_table_name, foreign_key_column, referenced_table_pk
):
    cur = conn.cursor()
    try:
        cur.execute(
            f'ALTER TABLE "{new_table_name}" DROP CONSTRAINT IF EXISTS "{old_table_name}{foreign_key_column}_fkey"'
        )

        cur.execute(
            f'ALTER TABLE "{new_table_name}" ADD CONSTRAINT "{new_table_name}{foreign_key_column}_fkey" FOREIGN KEY ("{foreign_key_column}") REFERENCES "{referenced_table_pk}"'
        )
        conn.commit()
        print(f"Foreign key updated in {new_table_name}")
    except Exception as e:
        conn.rollback()
        print(f"Error updating foreign key: {e}")
    cur.close()


copied_weeks_table = create_table_copy("Weeks")
copied_professors_table = create_table_copy("Professors")
copied_subjects_table = create_table_copy("Subjects")
copied_rooms_table = create_table_copy("Rooms")
copied_courses_table = create_table_copy("Courses")
copied_comments_table = create_table_copy("Comments")
copied_ratings_table = create_table_copy("Ratings")


update_foreign_keys(
    "Subjects", copied_subjects_table, "professor_id", copied_professors_table
)
update_foreign_keys(
    "Courses", copied_courses_table, "subject_id", copied_subjects_table
)
update_foreign_keys("Courses", copied_courses_table, "room_id", copied_rooms_table)
update_foreign_keys(
    "Comments", copied_comments_table, "subject_id", copied_subjects_table
)
update_foreign_keys(
    "Ratings", copied_ratings_table, "subject_id", copied_subjects_table
)
cur = conn.cursor()
cur.execute(f'TRUNCATE "Ratings"')
cur.execute(f'TRUNCATE "Weeks"')
conn.commit()
cur.close()
conn.close()
