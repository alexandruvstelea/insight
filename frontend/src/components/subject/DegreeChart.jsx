"use client";
import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
ChartJS.register(ArcElement, Tooltip, Legend);

export default function DegreeChart() {
  const dataAvailable = false;
  const data = {
    labels: dataAvailable ? ["1-4", "5-6", "7-8", "9-10"] : ["Nu există date"],
    datasets: [
      {
        label: "note",
        data: dataAvailable ? [12, 19, 3, 5] : [1],
        backgroundColor: dataAvailable
          ? [
              "rgba(255, 99, 132, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(54, 162, 235, 1)",
            ]
          : ["rgba(192, 192, 192, 1)"],
        borderColor: dataAvailable
          ? [
              "rgba(255, 99, 132, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(54, 162, 235, 1)",
            ]
          : ["rgba(192, 192, 192, 1)"],
        borderWidth: 0.5,
      },
    ],
  };
  const options = {
    plugins: {
      tooltip: {
        enabled: dataAvailable ? true : false,
      },
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
