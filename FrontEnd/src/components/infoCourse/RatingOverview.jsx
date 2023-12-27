import ProgressContainer from "./ProgressContainer";
import StarRating from "./StarRating";
import React, { useState, useEffect } from 'react';
import styles from './ratingOverview.module.css'

export default function RatingOverview({ subjectId, onError }) {
  const [error404, setError404] = useState(false);
  const [data, setData] = useState({});

  async function fetchRatingData(subjectId, setData) {

    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/ratingsnumber/${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/ratingsnumber_archive/${selectedYear}/${subjectId}` }

    try {
      const response = await fetch(url, { method: "GET" });

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