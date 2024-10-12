"use client";
import styles from "./page.module.css";
import { Line } from "react-chartjs-2";
import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
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

interface LineChartProps {
  ratingsData: RatingsData;
  title: string;
}

export default function LineChart({ ratingsData, title }: LineChartProps) {
  const labels = Object.keys(ratingsData).map(
    (key) => `Sapt. ${key.slice(-2).replace("_", "")}`
  );

  const clarityData = Object.values(ratingsData).map((item) => item.clarity);
  const interactivityData = Object.values(ratingsData).map(
    (item) => item.interactivity
  );
  const relevanceData = Object.values(ratingsData).map(
    (item) => item.relevance
  );
  const comprehensionData = Object.values(ratingsData).map(
    (item) => item.comprehension
  );
  const overallData = Object.values(ratingsData).map((item) => item.overall);

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

  const chartData = {
    labels,
    datasets: [
      {
        label: "Claritate",
        data: clarityData,
        borderColor: "rgba(5, 145, 248, 0.75)",
        backgroundColor: "rgba(5, 145, 248, 0.75)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
      },
      {
        label: "Relevanta",
        data: relevanceData,
        borderColor: "rgba(0, 169, 165, 0.75)",
        backgroundColor: "rgba(0, 169, 165, 0.75)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
      },
      {
        label: "Interactivitate",
        data: interactivityData,
        borderColor: "rgba(117, 220, 159, 0.75)",
        backgroundColor: "rgba(117, 220, 159, 0.75)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
      },

      {
        label: "Intelegere",
        data: comprehensionData,
        borderColor: "rgba(39, 223, 243, 0.75)",
        backgroundColor: "rgba(39, 223, 243, 0.75)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
      },
      {
        label: "Medie",
        data: overallData,
        borderColor: "rgba(0, 91, 234, 1)",
        backgroundColor: "rgba(0, 91, 234, 1)",
        borderWidth: 5,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 0,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
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
      y: {
        beginAtZero: true,
        max: 5,
      },
    },
  };

  return (
    <div className={styles.lineChartContainer}>
      <h1>{title}</h1>
      <Line
        data={chartData}
        options={chartOptions}
        className={styles.lineChart}
      />
    </div>
  );
}
