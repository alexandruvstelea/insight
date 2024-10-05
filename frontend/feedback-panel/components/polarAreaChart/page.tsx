"use client";
import styles from "./page.module.css";
import { PolarArea } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  ArcElement,
  Tooltip,
  Legend,
  scales,
} from "chart.js";

ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend);

interface PolarAreaChart {
  clarity: number;
  relevance: number;
  interactivity: number;
  comprehension: number;
  title: string;
}

export default function PolarAreaChart({
  clarity,
  relevance,
  interactivity,
  comprehension,
  title,
}: PolarAreaChart) {
  const chartData = {
    labels: ["Claritate", "Relevanta", "Interactivitate", "Intelegere"],
    datasets: [
      {
        label: "Recenzii profesor",
        data: [clarity, relevance, interactivity, comprehension],
        backgroundColor: [
          "rgba(0, 255, 255, 0.5)", // Claritate
          "rgba(31, 81, 255, 0.5)", //Relevanta
          "rgba(64, 224, 208,0.5)", //Interactivitate
          "rgba(63, 0, 255, 0.5)", //Intelegere
        ],
        borderColor: [
          "rgba(0, 255, 255, 0.8)",
          "rgba(31, 81, 255, 0.8)",
          "rgba(64, 224, 208,0.8)",
          "rgba(63, 0, 255, 0.8)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        fontColor: "black",
        position: "bottom" as const,
        align: "center" as const,
        labels: {
          color: "black",
        },
      },
    },
    scales: {
      r: {
        min: 0,
        max: 5,
      },
    },
  };

  return (
    <div className={styles.polarChartContainer}>
      <h1>{title}</h1>
      <PolarArea
        data={chartData}
        options={chartOptions}
        className={styles.polarChart}
      />
    </div>
  );
}
