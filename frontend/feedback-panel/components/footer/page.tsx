import styles from "./page.module.css";

export function Footer() {
  return (
    <>
      <div className={styles.footer}>
        ©&nbsp;
        <a
          href="https://alexandrustelea.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          Alexandru Stelea
        </a>
        &nbsp;&&nbsp;
        <a
          href="https://www.linkedin.com/in/cristianandreisava"
          target="_blank"
          rel="noopener noreferrer"
        >
          Andrei Sava
        </a>
      </div>
    </>
  );
}
