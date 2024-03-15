import LinearProgress from "@mui/material/LinearProgress";
import styles from "./progressContainer.module.css";
export default function ProgressContainer({ name, average }) {
  const normalizedAverage = (average / 5) * 100;
  return (
    <>
      <div className={styles.progressContainer}>
        <span className={styles.textM}>{name}</span>
        <div className={styles.progressBar}>
          <LinearProgress
            style={{ height: "7px" }}
            variant="determinate"
            value={normalizedAverage}
          />
        </div>
        <span className={styles.textMM}>5</span>
      </div>
    </>
  );
}
