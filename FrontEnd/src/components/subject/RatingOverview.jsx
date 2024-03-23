"use server";
import React from "react";
import styles from "./ratingOverview.module.css";
import ProgressContainer from "./ProgressContainer";
import StarRating from "./StarRating";

export default async function RatingOverview({ ratingsAverage }) {
  const { clarity, comprehension, interactivity, relevance, overall } =
    ratingsAverage;

  return (
    <>
      <div className={styles.ratingOverview}>
        <h1 className={styles.title}>Media totala</h1>
        <ProgressContainer name="Claritate" average={clarity} />
        <ProgressContainer name="Înţelegere" average={comprehension} />
        <ProgressContainer name="Interactivitate" average={interactivity} />
        <ProgressContainer name="Relevanţă" average={relevance} />
        <StarRating overall={overall} />
      </div>
    </>
  );
}
