import styles from "./page.module.css";

export function NoData() {
  return (
    <>
      <div className={styles.pageContainer}>
        <h1>Nu există date.</h1>
      </div>
    </>
  );
}
