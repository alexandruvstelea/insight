import React from "react";
import Rating from "@mui/material/Rating";
import styles from "./starRatings.module.css";

export default function StarRating({ overall }) {
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
              color: "#1976D2",
            },
          }}
          readOnly
        />
      </div>
    </>
  );
}
