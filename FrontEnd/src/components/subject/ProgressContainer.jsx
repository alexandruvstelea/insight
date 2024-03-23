"use server";
import React from "react";
import styles from "./progressContainer.module.css";
import LinearProgress from "@mui/material/LinearProgress";
export default async function ProgressContainer({ name, average }) {
  const normalizedAverage = (average / 5) * 100;
  return (
    <>
      <div className={styles.progressContainer}>
        <span className={styles.textLeft}>{name}</span>
        <div className={styles.progressBar}>
          <LinearProgress
            style={{ height: "7px" }}
            variant="determinate"
            value={normalizedAverage}
          />
        </div>
        <span className={styles.textRight}>{average}</span>
      </div>
    </>
  );
}
