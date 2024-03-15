"use client";
import React, { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function BarChart({ graphData }) {
  const isWindowAvailable = typeof window !== "undefined";
  const [viewportWidth, setViewportWidth] = useState(
    isWindowAvailable ? window.innerWidth : null
  );

  const chartOrientation = viewportWidth < 600 ? "horizontalBar" : "bar";

  useEffect(() => {
    if (isWindowAvailable) {
      function handleResize() {
        setViewportWidth(window.innerWidth);
      }

      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, [isWindowAvailable]);

  const colors = [
    "rgba(75, 192, 192, 0.5)",
    "rgba(255, 99, 132, 0.5)",
    "rgba(54, 162, 235, 0.5)",
    "rgba(255, 206, 86, 0.5)",
    "rgba(153, 102, 255, 0.5)",
  ];

  const characteristics = [
    "overall",
    "clarity",
    "comprehension",
    "interactivity",
    "relevance",
  ];

  const characteristicData = {};
  characteristics.forEach((characteristic) => {
    characteristicData[characteristic] = Object.keys(graphData).map(
      (week) => graphData[week][characteristic]
    );
  });

  const options = {
    indexAxis: chartOrientation === "horizontalBar" ? "y" : "x",
    responsive: true,

    plugins: {
      legend: {
        position: "top",
        onClick: () => {},
      },
      title: {
        display: true,
        text: "Chart.js Bar Chart",
      },
    },
    scales: {
      x: {
        ticks: {
          stepSize: 1,
        },
        beginAtZero: true,
        suggestedMax: 5,
        title: {
          display: true,
          text: "Saptamana",
          font: {
            size: 14,
          },
        },
      },
      y: {
        title: {
          display: true,
          text: "Media",
          font: {
            size: 14,
          },
        },
        ticks: {
          stepSize: 1,
        },
        beginAtZero: true,
        suggestedMax: 5,
      },
    },

    elements: {
      bar: {
        borderWidth: 1,
        borderColor: "rgba(0,0,0,0.4)",
      },
    },
  };

  const labels = [];
  for (let i = 1; i <= 14; i++) {
    labels.push(`${i}S`);
  }

  const [selectedDataset, setSelectedDataset] = useState("overall");

  const handleDatasetChange = (event) => {
    setSelectedDataset(event.target.value);
  };

  const datasets = characteristics.map((characteristic, index) => ({
    label: characteristic,
    data: characteristicData[characteristic],
    backgroundColor: colors[index],
  }));

  const selectedData = datasets.find(
    (dataset) => dataset.label === selectedDataset
  );

  return (
    <div>
      <select value={selectedDataset} onChange={handleDatasetChange}>
        {characteristics.map((characteristic, index) => (
          <option key={index} value={characteristic}>
            {characteristic}
          </option>
        ))}
      </select>
      <Bar
        options={options}
        data={{ labels, datasets: [selectedData] }}
        width={800}
        height={550}
      />
    </div>
  );
}
