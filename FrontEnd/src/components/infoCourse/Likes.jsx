import React from 'react';
import styles from './likes.module.css'
import { Chart } from "react-google-charts";

export default function Likes({ likesData }) {

  const noData = likesData.like === 0 && likesData.dislike === 0;

  const data = noData
    ? [
      ["Status", "Voturi"],
      ["Nu exista voturi", 1],
    ]
    : [
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
    slices: noData
      ? { 0: { color: '#BEBEBE' } }
      : {
        0: { offset: 0.06 },
        1: { offset: 0.06 },
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