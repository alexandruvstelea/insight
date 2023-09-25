const ctx = document.getElementById('myChart').getContext('2d');

const myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Sapt 1', 'Sapt 2', 'Sapt 3', 'Sapt 4', 'Sapt 5','Sapt 6','Sapt 7','Sapt 8','Sapt 9','Sapt 10','Sapt 11','Sapt 12','Sapt 13','Sapt 14'],
    datasets: [{
      label: 'Note',
      data: [0,3,4,4,4,4,2,1,5,5,5,2,1,5],
      backgroundColor: '#4070F4',
      borderColor: 'blue',
      borderWidth: 1,
    }],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});