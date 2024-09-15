import styles from "./page.module.css";

interface infoBox {
  title: string;
  content: string;
}

export function InfoBox({ title, content }: infoBox) {
  return (
    <div className={styles.infoBox}>
      <h1>{title}</h1>
      <h2>{content}</h2>
    </div>
  );
}
