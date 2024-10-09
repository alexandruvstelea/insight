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
  ratings_data: RatingsData;
  rating_type: keyof RatingsData[keyof RatingsData];
  label: string;
}

export default function BarChart({
  ratings_data,
  rating_type,
  label,
}: BarChartProps) {
  const labels = Object.keys(ratings_data).map(
    (key) => `Sapt. ${key.slice(-2).replace("_", "")}`
  );
  const data = Object.values(ratings_data).map((item) => item[rating_type]);

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
    labels,
    datasets: [
      {
        label: label,
        data,
        backgroundColor: "rgba(0, 91, 234, 0.75)",
        borderColor: "rgba(0, 91, 234, 1)",
        borderWidth: 2,
        borderRadius: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
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
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
}
