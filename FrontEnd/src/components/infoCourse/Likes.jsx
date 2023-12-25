import React, { useEffect, useState } from 'react';
import styles from './likes.module.css'
import { Chart } from "react-google-charts";

export default function Likes({ subjectId }) {
  const [likesData, setLikesData] = useState({ like: 0, dislike: 0 });

  const fetchLikes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/nr_likes/${subjectId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setLikesData(data);

    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  useEffect(() => {
    fetchLikes()
  }, [subjectId]);


  const data = [
    ["Like/Dislike", "Voturi"],
    ["Like", likesData.like],
    ["Dislike", likesData.dislike],
  ];


  const options = {
    is3D: true,
    backgroundColor: 'transparent',
    pieSliceTextStyle: {
      fontSize: 11,

    },
    slices: {
      0: { offset: 0.1 },
      1: { offset: 0.1 },

    },

    legend: {
      position: 'top',
      alignment: 'center',
    }

  };

  return (
    <>
      <div className={styles.container}>
        <div>
          <Chart
            chartType="PieChart"
            data={data}
            options={options}
            width={"300px"}
            height={"300px"}
          />
        </div>
      </div>

    </>
  )
}