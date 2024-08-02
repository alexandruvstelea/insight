"use server";
import React from "react";
import styles from "./starRatings.module.css";
import Rating from "@mui/material/Rating";

export default async function StarRating({ overall, color }) {
  return (
    <>
      <div className={styles.starContent}>
        <span className={styles.averageRating}>{overall}</span>
        <Rating
          size="large"
          name="half-rating-read"
          value={parseFloat(overall)}
          precision={0.1}
          sx={{
            "& .MuiRating-iconFilled": {
              color: color,
            },
          }}
          readOnly
        />
      </div>
    </>
  );
}
