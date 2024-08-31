import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";

interface FacultySelector {
  facultyID: number;
  facultyName: string;
  svgPath: string;
}

export default function FacultySelector({
  facultyID,
  facultyName,
  svgPath,
}: FacultySelector) {
  return (
    <div className={styles.facultySelector}>
      <Image
        src={svgPath}
        width={88}
        height={88}
        alt="Faculty logo"
        className={styles.facultyLogo}
      />
      <h1>{facultyName}</h1>
      <Link
        href={{
          pathname: `/panel/${facultyID}`,
        }}
        className={styles.arrowButton}
      >
        &#x27F6;
      </Link>
    </div>
  );
}
