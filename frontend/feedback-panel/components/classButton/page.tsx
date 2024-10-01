import styles from "./page.module.css";
import Link from "next/link";

interface ClassButton {
  classId: number;
  className: string;
  classType: string;
  facultyId: number;
  professorId: number;
}

export default function ClassButton({
  classId,
  className,
  classType,
  facultyId,
  professorId,
}: ClassButton) {
  return (
    <Link
      href={{
        pathname: `/panel/${facultyId}/${professorId}/${classType}/${classId}`,
      }}
      className={styles.classButton}
    >
      <h1>{className}</h1>
    </Link>
  );
}
