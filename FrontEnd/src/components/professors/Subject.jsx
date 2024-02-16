import styles from "./subject.module.css";
import { useRouter } from "next/navigation";
export default function Subject({ subject }) {
  const router = useRouter();
  function handleClick(id) {
    router.push(`/professors/infoCourse?subjectId=${id}`);
  }

  return (
    <li>
      <button
        onClick={() => handleClick(subject.id)}
        className={styles.buttonCourses}
        role="button"
      >
        {subject.name}
      </button>
    </li>
  );
}
