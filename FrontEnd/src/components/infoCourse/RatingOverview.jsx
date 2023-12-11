import ProgressContainer from "./ProgressContainer";
import StarRating from "./StarRating";
import React, { useState, useEffect } from 'react';
import styles from './ratingOverview.module.css'

export default function RatingOverview({ subjectId, onError }) {
  const [error404, setError404] = useState(false);
  const [data, setData] = useState({});

  async function fetchRatingData(subjectId, setData) {

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/ratingsnumber/${subjectId}`, { method: "GET" });

      if (!response.ok) {
        if (response.status === 404) {
          setError404(true);
        }
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      const total = Object.values(data).reduce((acc, val) => acc + val, 0);
      const percentageData = Object.fromEntries(
        Object.entries(data).map(([key, value]) => [key, parseFloat((value / total * 100).toFixed(1))])
      );
      setData(percentageData);
    } catch (err) {
      console.error(err);
    }
  }
  useEffect(() => {
    fetchRatingData(subjectId, setData);
  }, [subjectId]);

  useEffect(() => {
    if (error404) {
      onError(true);
    }
  }, [error404]);



  return (
    <>
      <div className={styles.ratingOverview}>
        <ProgressContainer name="Nota 1" percentage={data['1_rating']} />
        <ProgressContainer name="Nota 2" percentage={data['2_rating']} />
        <ProgressContainer name="Nota 3" percentage={data['3_rating']} />
        <ProgressContainer name="Nota 4" percentage={data['4_rating']} />
        <ProgressContainer name="Nota 5" percentage={data['5_rating']} />

        <StarRating subjectId={subjectId} />
      </div>
    </>
  )
}