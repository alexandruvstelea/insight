import styles from "./footer.module.css";
export default function Footer() {
  return (
    <>
      <footer className={styles.footer}>
        <div className={styles.footerAuthors}>
          ©{" "}
          <a
            href="https://alexandrustelea.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            Alexandru Stelea
          </a>{" "}
          &{" "}
          <a
            href="https://www.linkedin.com/in/cristianandreisava"
            target="_blank"
            rel="noopener noreferrer"
          >
            Andrei Sava
          </a>
        </div>
      </footer>
    </>
  );
}
