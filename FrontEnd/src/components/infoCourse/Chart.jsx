

'use client'
import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, } from 'chart.js';
import { Bar } from 'react-chartjs-2';
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
        },
        beginAtZero: true,
        suggestedMax: 5,
      },
      y: {
        ticks: {
          stepSize: 1,
        },
        beginAtZero: true,
        suggestedMax: 5,
      }
    }
  };
}

export default function BarChart({ subjectId, onError }) {
  const [error404, setError404] = useState(false);
  const isWindowAvailable = typeof window !== 'undefined';
  const [viewportWidth, setViewportWidth] = useState(isWindowAvailable ? window.innerWidth : null);

  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: '#4070F4',
      borderColor: 'blue',
      borderWidth: 1,
    }],
  });
  const chartOrientation = viewportWidth < 600 ? 'horizontalBar' : 'bar';



  useEffect(() => {
    if (isWindowAvailable) {
      function handleResize() {
        setViewportWidth(window.innerWidth);
      }

      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [isWindowAvailable]);





  async function fetchSubjectGraphData(subjectId) {

    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/graph?subject_id=${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/graph_archive/${selectedYear}?subject_id=${subjectId}` }

    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        if (response.status === 404) {
          setError404(true);
        }
        throw new Error(`HTTP error: ${response.status}`);
      }

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
  useEffect(() => {
    if (subjectId) {
      fetchSubjectGraphData(subjectId);
    }
  }, [subjectId]);

  useEffect(() => {
    if (error404) {
      onError(true);
    }
  }, [error404]);



  return (
    <Bar options={getOptions(chartOrientation)} data={chartData} />
  )


}
