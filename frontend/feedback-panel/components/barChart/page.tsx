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
  [key: string]: {
    clarity: number;
    interactivity: number;
    relevance: number;
    comprehension: number;
    overall: number;
  };
}

interface BarChartProps {
  ratingsData: RatingsData;
  ratingType: keyof RatingsData[keyof RatingsData];
  label: string;
}

export default function BarChart({
  ratingsData,
  ratingType,
  label,
}: BarChartProps) {
  const labels = Object.keys(ratingsData).map(
    (key) => `Sapt. ${key.slice(-2).replace("_", "")}`
  );
  const data = Object.values(ratingsData).map((item) => item[ratingType]);

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
    overall: {
      background: "rgba(0, 91, 234, 0.75)",
      border: "rgba(0, 91, 234, 1)",
    },
    interactivity: {
      background: "rgba(117, 220, 159, 0.75)",
      border: "rgba(117, 220, 159, 1)",
    },
    relevance: {
      background: "rgba(0, 169, 165, 0.75)",
      border: "rgba(0, 169, 165, 1)",
    },
    comprehension: {
      background: "rgba(39, 223, 243, 0.75)",
      border: "rgba(39, 223, 243, 1)",
    },
    clarity: {
      background: "rgba(5, 145, 248, 0.75)",
      border: "rgba(5, 145, 248, 1)",
    },
  };

  const { background, border } = colorMapping[ratingType];

  const chartData = {
    labels,
    datasets: [
      {
        label: label,
        data,
        backgroundColor: background,
        borderColor: border,
        borderWidth: 2,
        borderRadius: 4,
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
      y: {
        beginAtZero: true,
        max: 5,
      },
    },
  };

  return (
    <div className={styles.barChartContainer}>
      <Bar
        data={chartData}
        options={chartOptions}
        className={styles.barChart}
      />
    </div>
  );
}
