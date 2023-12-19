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
      console.log(data)
      setLikesData(data);

      console.log(likesData)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  useEffect(() => {
    fetchLikes()
  }, [subjectId]);


  const data = [
    ["Like/Dislike", "Voturi"],
    ["like", likesData.like],
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
  };

  return (
    <>
      <div className={styles.container}>
        <div>
          <Chart
            chartType="PieChart"
            data={data}
            options={options}
            width={"320px"}
            height={"320px"}
          />
        </div>
      </div>

    </>
  )
}