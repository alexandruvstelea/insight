import styles from "./page.module.css";

interface ScrollButton {
  text: string;
  scrollId: string;
}

export function ScrollButton({ text, scrollId }: ScrollButton) {
  return (
    <>
      <a className={styles.scrollButton} href={`#${scrollId}`}>
        {text}
      </a>
    </>
  );
}
