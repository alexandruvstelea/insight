import styles from "./page.module.css";
import Image from "next/image";

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
      <h1>
        Feedback
        <br />
        {facultyName}
      </h1>
      <a href="#">&#x2192;</a>
    </div>
  );
}
