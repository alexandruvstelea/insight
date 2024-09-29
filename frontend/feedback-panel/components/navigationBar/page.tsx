import styles from "./page.module.css";
import Link from "next/link";

interface NavigationBar {
  facultyAbbreviation?: string;
}

export function NavigationBar({ facultyAbbreviation }: NavigationBar) {
  return (
    <div className={styles.navBar}>
      {facultyAbbreviation ? (
        <Link
          href={{
            pathname: "/",
          }}
          className={styles.link}
        >
          <h1>
            inSight <span>{` ${facultyAbbreviation}`}</span>
          </h1>
        </Link>
      ) : (
        <Link
          href={{
            pathname: "/",
          }}
          className={styles.link}
        >
          <h1>inSight</h1>
        </Link>
      )}
    </div>
  );
}
