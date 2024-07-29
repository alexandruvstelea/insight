"use client";
import React, { useState, useEffect } from "react";
import styles from "./chart.module.css";
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

export default function BarChart({ graphData, colors }) {
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

  const characteristics = [
    ["overall", "Total"],
    ["clarity", "Claritate"],
    ["comprehension", "Înțelegere"],
    ["interactivity", "Interactivitate"],
    ["relevance", "Relevanță"],
  ];

  const characteristicData = {};
  characteristics.forEach((characteristic) => {
    characteristicData[characteristic[0]] = Object.keys(graphData).map(
      (week) => graphData[week][characteristic[0]]
    );
  });

  const options = {
    indexAxis: chartOrientation === "horizontalBar" ? "y" : "x",
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
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
          text: "Săptămâna",
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
  };
  const axisLabels =
    chartOrientation === "horizontalBar"
      ? ["Media", "Săptămâna"]
      : ["Săptămâna", "Media"];
  options.scales.x.title.text = axisLabels[0];
  options.scales.y.title.text = axisLabels[1];

  const labels = [];
  for (let i = 1; i <= 14; i++) {
    labels.push(`S${i}`);
  }

  const [selectedDataset, setSelectedDataset] = useState("Total");

  const handleDatasetChange = (label) => {
    setSelectedDataset(label);
  };

  const handleDatasetChangeSelect = (event) => {
    setSelectedDataset(event.target.value);
  };

  const datasets = characteristics.map((characteristic, index) => ({
    label: characteristic[1],
    data: characteristicData[characteristic[0]],
    backgroundColor: colors[index],
  }));

  const selectedData = datasets.find(
    (dataset) => dataset.label === selectedDataset
  );

  return (
    <>
      <div className={styles.selectContainer}>
        <select
          className={styles.select}
          value={selectedDataset}
          onChange={handleDatasetChangeSelect}
        >
          {characteristics.map((characteristic, index) => (
            <option
              className={styles.option}
              key={index}
              value={characteristic[1]}
            >
              {characteristic[1]}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.chartContainer}>
        <Bar
          options={options}
          data={{ labels, datasets: [selectedData] }}
          width="600"
          height="250"
        />
      </div>

      <div className={styles.buttonsContainer}>
        {characteristics.map((characteristic, index) => (
          <div
            key={index}
            onClick={() => handleDatasetChange(characteristic[1])}
            className={`${styles.button} ${
              selectedDataset === characteristic[1] ? styles.selectedButton : ""
            }`}
            style={{ backgroundColor: colors[index] }}
          >
            {characteristic[1]}
          </div>
        ))}
      </div>
    </>
  );
}
