import styles from "./subjectsList.module.css";
import Link from "next/link";
export default function SubjectsList({ subjects }) {
  // const router = useRouter();
  // function handleClick(id) {
  //   router.push(`/professors/infoCourse?subjectId=${id}`);
  // }

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
                  href={`/professors/${subject.id}`}
                >
                  {subject.name}
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
