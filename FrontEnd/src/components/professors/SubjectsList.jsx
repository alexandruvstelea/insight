import React from "react";
import styles from "./subjectsList.module.css";
import Link from "next/link";

export default function SubjectsList({
  subjects,
  first_name,
  last_name,
  archive = false,
  year = false,
}) {
  return (
    <>
      <h1 className={styles.titleCurs}>Cursuri</h1>
      {subjects.length != 0 ? (
        <>
          <ul className={styles.coursesList}>
            {subjects.map((subject) => (
              <li key={subject.id}>
                <Link
                  className={styles.buttonCourses}
                  href={
                    archive && year
                      ? {
                          pathname: `/professors/${subject.id}/archive`,
                        }
                      : { pathname: `/professors/${subject.id}` }
                  }
                  onClick={() => {
                    sessionStorage.setItem(
                      "name",
                      `${first_name} ${last_name}`
                    );
                  }}
                >
                  {subject.name.length > 27
                    ? subject.abbreviation
                    : subject.name}
                </Link>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <>
          <ul className={styles.coursesList}>
            <li>Nu exist&#259; cursuri.</li>
          </ul>
        </>
      )}
    </>
  );
}
