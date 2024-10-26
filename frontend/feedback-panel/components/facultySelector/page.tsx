import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";

interface FacultySelector {
  facultyAbbreviation: string;
  facultyName: string;
  svgPath: string;
}

export default function FacultySelector({
  facultyAbbreviation,
  facultyName,
  svgPath,
}: FacultySelector) {
  return (
    <div className={styles.gradientBox}>
      <div className={styles.facultySelector}>
        <Link
          href={{
            pathname: `/feedback/${facultyAbbreviation}`,
          }}
          className={styles.selectorLink}
        >
          <Image
            src={svgPath}
            width={88}
            height={88}
            alt="Faculty logo"
            className={styles.facultyLogo}
          />
          <h1>{facultyName}</h1>
          <Image
            height={40}
            width={40}
            alt="Arrow symbol"
            src={"/svg/arrow-forward.svg"}
            className={styles.arrowButton}
          />
        </Link>
      </div>
    </div>
  );
}
