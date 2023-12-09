import React, { useEffect, useState } from 'react';
import Rating from '@mui/material/Rating';
import styles from './starRatings.module.css'

export default function StarRating({ subjectId }) {
  const [averageRating, setAverageRating] = useState(0);

  async function fetchRatingAverage(subjectId) {
    const url = `${process.env.REACT_APP_API_URL}/rating/${subjectId}`;

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAverageRating((data.response * 1).toFixed(2));

    } catch (err) {
      console.error('There has been a problem with your fetch operation:', err);
    }
  }

  useEffect(() => {
    fetchRatingAverage(subjectId);
  }, [subjectId]);

  return (
    <>
      <div className={styles.starContent}>
        <span className={styles.averageRating}>{averageRating}</span>
        <Rating size='large' name="half-rating-read" value={parseFloat(averageRating)} precision={0.1} readOnly />
      </div>
    </>
  );
}