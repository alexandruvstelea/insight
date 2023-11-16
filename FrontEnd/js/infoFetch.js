
function fetchRatingData(subjectId) {
  const url = `${URL}/ratingsnumber/${subjectId}`;

  fetch(url, { method: "GET" })
    .then((response) => {
      if (response.status === 404) {
        alert("Data not found for the given subject ID");
        throw new Error('404 Not Found');
      }
      return response.json();
    })
    .then((data) => {
      setPercentages(calculateRatingsPercentages(data));
    })
    .catch((err) => {
      console.error(err);
    });
}
function fetchRatingAverage(subjectId) {
  const url = `${URL}/rating/${subjectId}`;

  fetch(url, { method: "GET" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      coloreazaStelutele(data.response);
    })
    .catch((err) => {
      console.error('There has been a problem with your fetch operation:', err);
    });
}
function fetchGraphData(subjectId) {
  const url = `${URL}/graph?subject_id=${subjectId}`;

  fetch(url, { method: "GET" })
    .then((response) => {
      if (!response.ok) {
        if (response.status === 404) {
          alert("No data available for the requested graph");
          throw new Error('404 Not Found');
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }
      return response.json();
    })
    .then(data => {
      console.log(data)
      const weeks = Object.keys(data).map(key => parseInt(key.split('_')[1], 10));
      const minWeek = Math.min(...weeks);
      const maxWeek = Math.max(...weeks);
      const arrayLength = maxWeek - minWeek + 1;

      let array = new Array(arrayLength).fill(0);

      Object.keys(data).forEach(key => {
        const weekNumber = parseInt(key.split('_')[1], 10);
        const index = weekNumber - minWeek;
        array[index] = data[key];
      });
      console.log(array)
      myChartData(array);
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });
}



document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  const subjectId = urlParams.get('subjectId');
  fetchRatingData(subjectId);
  fetchRatingAverage(subjectId);
  fetchGraphData(subjectId);
  console.log(subjectId)
});

function calculateRatingsPercentages(ratings) {

  const totalRatings = Object.values(ratings).reduce((acc, numRatings) => acc + numRatings, 0);
  const ratingsPercentages = [];

  for (let i = 1; i <= 5; i++) {
    const ratingKey = `${i}_rating`;
    const count = ratings[ratingKey];
    const percentage = (count / totalRatings) * 100;
    ratingsPercentages.push(percentage);
  }

  return ratingsPercentages;
}

