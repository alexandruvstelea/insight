'use client'
import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import styles from './chart.module.css'
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function getOptions(chartOrientation) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: chartOrientation === 'horizontalBar' ? 'y' : 'x',
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        ticks: {
          stepSize: 1,
          max: 5,
        },
        beginAtZero: true,
      },
      y: {
        ticks: {
          stepSize: 1,
          max: 5,
        },
        beginAtZero: true,
      }
    }
  };
}

export default function Chart({ subjectId }) {

  const isWindowAvailable = typeof window !== 'undefined';
  const [viewportWidth, setViewportWidth] = useState(isWindowAvailable ? window.innerWidth : null);
  const chartOrientation = viewportWidth < 500 ? 'horizontalBar' : 'bar';
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: '#4070F4',
      borderColor: 'blue',
      borderWidth: 1,
    }],
  });

  useEffect(() => {
    if (isWindowAvailable) {
      function handleResize() {
        setViewportWidth(window.innerWidth);
      }

      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [isWindowAvailable]);

  useEffect(() => {
    if (subjectId) {
      fetchSubjectGraphData(subjectId);
    }
  }, [subjectId]);



  async function fetchSubjectGraphData(subjectId) {
    const url = `${process.env.REACT_APP_API_URL}/graph?subject_id=${subjectId}`;
    try {
      const response = await fetch(url, { method: "GET" });
      const data = await response.json();

      const sortedWeeks = Object.keys(data).sort((a, b) => {
        return parseInt(a.split('_')[1], 10) - parseInt(b.split('_')[1], 10);
      });

      const weeksNumber = sortedWeeks.map(week => `Sapt ${week.split('_')[1]}`);
      const values = sortedWeeks.map(week => data[week]);

      setChartData(prevChartData => ({
        labels: weeksNumber,
        datasets: [{
          ...prevChartData.datasets[0],
          data: values,
        }]
      }));
    } catch (error) {
      console.error('Error fetching graph data:', error);
    }
  }

  return (
    <div className={styles.chartContainer}>
      <Bar options={getOptions(chartOrientation)} data={chartData} />
    </div>
  )


}
