import styles from "./page.module.css";

interface tutorialBox {
  step: string;
  content: string;
}

export function TutorialBox({ step, content }: tutorialBox) {
  return (
    <div className={styles.gradientBox}>
      <div className={styles.tutorialBox}>
        <h1>{step}&#x21b4;</h1>
        <h2>{content}</h2>
      </div>
    </div>
  );
}
