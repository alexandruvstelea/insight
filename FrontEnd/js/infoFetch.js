function fetchRatingData(subjectId) {
  const url = `http://127.0.0.1:5000/ratingsnumber/${subjectId}`;

  fetch(url, { method: "GET" })
    .then((response) => {    
      if (response.status === 404) {
        alert("Data not found for the given subject ID");
        // Aruncați o eroare pentru a opri executarea lanțului de promisiuni
        throw new Error('404 Not Found');
      }
      return response.json();
    })
    .then((data) => {
      setPercentages(calculateRatingsPercentages(data));
    })
    .catch((err) => {
      // Tratați orice eroare care apare în lanțul de promisiuni
      console.error(err);
    });
}
function fetchRatingAverage(subjectId) {
  const url = `http://127.0.0.1:5000/rating/${subjectId}`;

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
  const url = `http://127.0.0.1:5000/graph?subject_id=${subjectId}`;

  fetch(url, { method: "GET" })
    .then((response) => {
      if (!response.ok) {
        if (response.status === 404) {
          alert("No data available for the requested graph");
          // Aruncați o eroare pentru a opri executarea ulterioară
          throw new Error('404 Not Found');
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }
      return response.json();
    })
    .then(data => {
      let array = new Array(Object.keys(data).length).fill(0);
      Object.keys(data).forEach(key => {
        const weekNumber = parseInt(key.split('_')[1], 10) - 1;
        array[weekNumber] = data[key];
      });
      
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

