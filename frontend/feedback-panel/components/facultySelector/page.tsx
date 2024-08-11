import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";

interface FacultySelector {
  facultyName: string;
  svgPath: string;
}

export default function FacultySelector({
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
          pathname: "/panel/1",
          query: {
            facultyName: facultyName,
          },
        }}
        className={styles.arrowButton}
      >
        &#x27F6;
      </Link>
    </div>
  );
}
