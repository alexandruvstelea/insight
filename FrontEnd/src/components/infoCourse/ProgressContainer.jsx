import LinearProgress from '@mui/material/LinearProgress';
import styles from './progressContainer.module.css'
export default function ProgressContainer({ name, percentage }) {
  const MIN = 0;
  const MAX = 100;

  const calculatePercentage = (value) => ((value - MIN) * 100) / (MAX - MIN);
  return (
    <>
      <div className={styles.progressContainer}>
        <span className={styles.textM}>{name}</span>
        <div className={styles.progressBar}>
          <LinearProgress style={{ height: '7px' }} variant="determinate" value={calculatePercentage(percentage)} />
        </div>
        <span className={styles.textM} >{percentage}%</span>
      </div>
    </>
  )
}