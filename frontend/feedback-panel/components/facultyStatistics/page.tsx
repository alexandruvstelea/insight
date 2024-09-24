"use client";
import { useEffect, useState } from "react";
import styles from "./page.module.css";

interface FacultyStatisticsProps {
  statistic: number;
  name: string;
}

export default function FacultyStatistics({
  statistic,
  name,
}: FacultyStatisticsProps) {
  const [displayedStatistic, setDisplayedStatistic] = useState(0);

  const formatStatistic = (stat: number) => {
    return stat > 999 ? (stat / 1000).toFixed(1) + "k" : stat.toString();
  };

  useEffect(() => {
    const duration = 1500;
    const increment = statistic / (duration / 16);
    let current = 1;

    const animateStatistic = () => {
      current += increment;
      if (current < statistic) {
        setDisplayedStatistic(Math.floor(current));
        requestAnimationFrame(animateStatistic);
      } else {
        setDisplayedStatistic(statistic);
      }
    };

    requestAnimationFrame(animateStatistic);
  }, [statistic]);

  return (
    <div className={styles.facultyStatistic}>
      <h1>{formatStatistic(displayedStatistic)}</h1>
      <h2>{name}</h2>
    </div>
  );
}
