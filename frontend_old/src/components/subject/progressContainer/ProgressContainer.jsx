"use client";
import React from "react";
import styles from "./progressContainer.module.css";
import LinearProgress from "@mui/material/LinearProgress";
import { createTheme, ThemeProvider } from "@mui/material/styles";

export default function ProgressContainer({ name, average, color }) {
  const normalizedAverage = (average / 5) * 100;
  const theme = createTheme({
    palette: {
      primary: {
        main: color,
      },
    },
  });
  return (
    <>
      <ThemeProvider theme={theme}>
        <div className={styles.progressContainer}>
          <span className={styles.textLeft}>{name}</span>
          <div className={styles.progressBar}>
            <LinearProgress
              style={{ height: "7px" }}
              variant="determinate"
              value={normalizedAverage}
              color="primary"
            />
          </div>
          <span className={styles.textRight}>{average}</span>
        </div>
      </ThemeProvider>
    </>
  );
}
