"use server";
import React from "react";
import styles from "./ratingOverview.module.css";
import ProgressContainer from "../progressContainer/ProgressContainer";
import StarRating from "../starRating/StarRating";

export default async function RatingOverview({ ratingsAverage, colors }) {
  const { clarity, comprehension, interactivity, relevance, overall } =
    ratingsAverage;

  return (
    <>
      <div className={styles.ratingOverview}>
        <h1 className={styles.title}>Media totală</h1>
        <ProgressContainer
          name="Claritate"
          average={clarity}
          color={colors[1]}
        />
        <ProgressContainer
          name="Înţelegere"
          average={comprehension}
          color={colors[2]}
        />
        <ProgressContainer
          name="Interactivitate"
          average={interactivity}
          color={colors[3]}
        />
        <ProgressContainer
          name="Relevanţă"
          average={relevance}
          color={colors[4]}
        />
        <StarRating overall={overall} color={colors[0]} />
      </div>
    </>
  );
}
