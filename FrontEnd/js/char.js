

const data = {
  labels: ['Sapt 1', 'Sapt 2', 'Sapt 3', 'Sapt 4', 'Sapt 5', 'Sapt 6', 'Sapt 7', 'Sapt 8', 'Sapt 9', 'Sapt 10', 'Sapt 11', 'Sapt 12', 'Sapt 13', 'Sapt 14'],
  datasets: [{
    label: 'Note',
    data: [2, 3, 4, 4, 1, 4, 1, 2, 5, 5, 5, 2, 2, 5],
    backgroundColor: '#4070F4',
    borderColor: 'blue',
    borderWidth: 1,
  }],
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  legend: { display: false },
  scales: {
    yAxes: [{
      ticks: {
        stepSize: 1,
          min:0,
          max:5,
      }
  }]
  },
};

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: options
});