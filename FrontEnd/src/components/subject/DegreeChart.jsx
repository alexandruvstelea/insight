"use client";
import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
ChartJS.register(ArcElement, Tooltip, Legend);

export default function DegreeChart() {
  const data = {
    labels: ["1-4", "5-6", "7-8", "9-10"],
    datasets: [
      {
        label: "note",
        data: [12, 19, 3, 5],
        backgroundColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(54, 162, 235, 1)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(54, 162, 235, 1)",
        ],
        borderWidth: 0.5,
      },
    ],
  };
  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          boxWidth: 10,
          font: {
            size: 12,
          },
        },
      },
      title: {
        display: true,
        text: "Notele studenților",
        font: {
          size: 16,
        },
      },
    },
  };

  return (
    <>
      <Pie data={data} options={options} />
    </>
  );
}
