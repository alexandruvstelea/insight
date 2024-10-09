"use client";
import styles from "./page.module.css";
import { PolarArea } from "react-chartjs-2";
import { useState, useEffect } from "react";
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
  const [fontSize, setFontSize] = useState(22);

  useEffect(() => {
    const updateFontSize = () => {
      if (window.innerWidth <= 600) {
        setFontSize(14);
      } else if (window.innerWidth <= 768) {
        setFontSize(18);
      } else {
        setFontSize(22);
      }
    };

    updateFontSize();

    window.addEventListener("resize", updateFontSize);

    return () => {
      window.removeEventListener("resize", updateFontSize);
    };
  }, []);

  const chartData = {
    labels: ["Claritate", "Relevanta", "Interactivitate", "Intelegere"],
    datasets: [
      {
        label: "Recenzii profesor",
        data: [clarity, relevance, interactivity, comprehension],
        backgroundColor: [
          "rgba(5, 145, 248, 0.75)", // Claritate
          "rgba(0, 169, 165, 0.75)", //Relevanta
          "rgba(117, 220, 159, 0.75)", //Interactivitate
          "rgba(39, 223, 243, 0.75)", //Intelegere
        ],
        borderColor: [
          "rgba(5, 145, 248, 0.9)", // Claritate
          "rgba(0, 169, 165, 0.9)", //Relevanta
          "rgba(117, 220, 159, 0.9)", //Interactivitate
          "rgba(39, 223, 243, 0.9)", //Intelegere
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
          font: {
            size: fontSize,
          },
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
