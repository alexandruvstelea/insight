import ProgressContainer from "./ProgressContainer";
import StarRating from "./StarRating";
import React from "react";
import styles from "./ratingOverview.module.css";

export default function RatingOverview({ ratingsAverage }) {
  const { clarity, comprehension, interactivity, relevance, overall } =
    ratingsAverage;
  return (
    <>
      <div className={styles.ratingOverview}>
        <ProgressContainer name="Clarity" average={clarity} />
        <ProgressContainer name="Comprehension" average={comprehension} />
        <ProgressContainer name="Interactivity" average={interactivity} />
        <ProgressContainer name="Relevance" average={relevance} />
        <StarRating overall={overall} />
      </div>
    </>
  );
}
