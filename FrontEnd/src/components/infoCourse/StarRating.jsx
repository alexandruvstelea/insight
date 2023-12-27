import React, { useEffect, useState } from 'react';
import Rating from '@mui/material/Rating';
import styles from './starRatings.module.css'

export default function StarRating({ subjectId }) {
  const [averageRating, setAverageRating] = useState(0);

  async function fetchRatingAverage(subjectId) {

    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/rating/${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/rating_archive/${selectedYear}/${subjectId}` }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
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
        <Rating
          size='large'
          name="half-rating-read"
          value={parseFloat(averageRating)}
          precision={0.1}
          sx={{
            '& .MuiRating-iconFilled': {
              color: '#1976D2',
            }
          }}
          readOnly />
      </div>
    </>
  );
}