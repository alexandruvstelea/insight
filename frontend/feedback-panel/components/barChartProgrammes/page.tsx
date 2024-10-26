"use client";
import styles from "./page.module.css";
import { Bar } from "react-chartjs-2";
import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface RatingsData {
  [key: string]: number;
}

interface BarChartProps {
  ratingsData: RatingsData;
  title: string;
}

export default function BarChartProgrammes({
  ratingsData,
  title,
}: BarChartProps) {
  const labels = Object.keys(ratingsData);
  const data = Object.values(ratingsData);

  const [fontSize, setFontSize] = useState(22);

  useEffect(() => {
    const updateFontSize = () => {
      if (window.innerWidth <= 600) {
        setFontSize(14);
      } else {
        setFontSize(16);
      }
    };

    updateFontSize();
    window.addEventListener("resize", updateFontSize);

    return () => {
      window.removeEventListener("resize", updateFontSize);
    };
  }, []);

  const colorMapping = {
    background: "rgba(0, 91, 234, 0.75)",
    border: "rgba(0, 91, 234, 1)",
  };

  const chartData = {
    labels,
    datasets: [
      {
        label: "Medie specializare",
        data,
        backgroundColor: colorMapping.background,
        borderColor: colorMapping.border,
        borderWidth: 2,
        borderRadius: 4,
        maxBarThickness: 50,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: "black",
          font: {
            size: fontSize,
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "black",
          font: {
            size: fontSize,
          },
        },
        title: {
          color: "black",
        },
      },
      y: {
        beginAtZero: true,
        max: 5,
        ticks: {
          color: "black",
          font: {
            size: fontSize - 3,
          },
        },
        title: {
          color: "black",
        },
      },
    },
  };

  return (
    <div className={styles.barChartContainer}>
      <h1>{title}</h1>
      <Bar
        data={chartData}
        options={chartOptions}
        className={styles.barChart}
      />
    </div>
  );
}
