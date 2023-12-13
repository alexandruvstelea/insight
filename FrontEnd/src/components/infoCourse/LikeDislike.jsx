import React, { useEffect, useState } from 'react';
import styles from './likeDislike.module.css'
import { Chart } from "react-google-charts";
import Image from 'next/image'
import Tooltip from '@mui/material/Tooltip';
import InfoIcon from '@mui/icons-material/Info';

export default function LikeDislike({ subjectId }) {
  const [likeDislikeData, setLikeDislikeData] = useState({ likes: 0, dislikes: 0 });

  const fetchLikesDislikes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/likes/${subjectId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      console.log(data)
      setLikeDislikeData(data);
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const addLikeDislike = async (likeDislike) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/likes/${subjectId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ like_dislike: likeDislike }),
      });
      if (!response.ok) {
        throw new Error('Failed to send vote');
      }
      await fetchLikesDislikes();
    } catch (err) {
      console.error('Error sending vote:', err);
    }
  };

  useEffect(() => {
    fetchLikesDislikes();
  }, [subjectId]);

  const data = [
    ["Like/Dislike", "Voturi"],
    ["like", likeDislikeData.likes],
    ["Dislike", likeDislikeData.dislikes],
  ];


  const options = {
    is3D: true,
    legend: "none",
    backgroundColor: 'transparent',
    pieSliceText: "value",
    pieSliceTextStyle: {
      fontSize: 22,

    },
    slices: {
      0: { offset: 0.1 },
      1: { offset: 0.1 },

    },
    chartArea: {

      width: "80%",
      height: "80%"
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
            width={"200px"}
            height={"200px"}
          />
        </div>


        <div className={styles.buttonsContainer}>
          <div onClick={() => addLikeDislike(true)} className={styles.logoSquare}>
            <Image width={50} height={50} alt="Like" src='/images/dislike.png'></Image>
          </div>
          <div onClick={() => addLikeDislike(false)} className={styles.logoSquare}>
            <Image width={50} height={50} alt="Like" src='/images/like.png'></Image>
          </div>
        </div>


        <div className={styles.infoSignContainer}>
          <Tooltip title='Nu se poate vota de pe aceeasi adresa IP' >
            <InfoIcon sx={{ color: '#0040C1', fontSize: 35 }} />
          </Tooltip>
        </div>

      </div>

    </>
  )
}