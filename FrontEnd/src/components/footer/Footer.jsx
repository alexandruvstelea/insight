import Link from "next/link";
import styles from "./footer.module.css";
export default function Footer() {
  const currentYear = 2024;

  return (
    <>
      <div className={styles.footer}>
        <div className={styles.footerAuthors}>
          ©{" "}
          <a
            href="https://alexandrustelea.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            Stelea Alexandru
          </a>{" "}
          &{" "}
          <a
            href="https://www.linkedin.com/in/cristianandreisava"
            target="_blank"
            rel="noopener noreferrer"
          >
            Sava Andrei
          </a>
        </div>
      </div>
    </>
  );
}
