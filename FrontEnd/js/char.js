
function myChartData(weekData){

  function getChartType() {
    return window.innerWidth < 500 ? 'horizontalBar' : 'bar';
  }
const data = {
  labels: ['Sapt 1', 'Sapt 2', 'Sapt 3', 'Sapt 4', 'Sapt 5', 'Sapt 6', 'Sapt 7', 'Sapt 8', 'Sapt 9', 'Sapt 10', 'Sapt 11', 'Sapt 12', 'Sapt 13', 'Sapt 14'],
  datasets: [{
    label: 'Note',
    data: weekData,
    backgroundColor: '#4070F4',
    borderColor: 'blue',
    borderWidth: 1,
  }],
};

function getOptions(chartType) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    legend: { display: false },
    scales: chartType === 'horizontalBar' ? {
      xAxes: [{ 
        ticks: {
          stepSize: 1,
          min: 0,
          max: 5,
        }
      }]
    } : {
      yAxes: [{ 
        ticks: {
          stepSize: 1,
          min: 0,
          max: 5,
        }
      }]
    }
  };
}
let chartType = getChartType();
  let options = getOptions(chartType);
  const ctx = document.getElementById('myChart').getContext('2d');
  let myChart = new Chart(ctx, {
    type: chartType,
    data: data,
    options: options
  });

  window.addEventListener('resize', function() {
    let newChartType = getChartType();
    if (newChartType !== chartType) {
      chartType = newChartType;
      options = getOptions(chartType);
      myChart.destroy();
      myChart = new Chart(ctx, { 
        type: chartType,
        data: data,
        options: options
      });
    }
  });
}