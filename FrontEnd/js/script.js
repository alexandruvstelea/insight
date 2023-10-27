function fetchProfessor() {
  const url = 'http://127.0.0.1:5000/professors'
  fetch(url, { method: "GET" })
    .then((response) => response.json())
    .then((complete_response) => addProfessor(complete_response))
    .catch((err) => { console.log(err) })
}


function fetchSubject(professor_id) {
  const url = `http://127.0.0.1:5000/subjects/${professor_id}`

  fetch(url, { method: "GET" })
    .then((response) => response.json())
    .then((complete_response) => addSubjects(complete_response, professor_id))
    .catch((err) => { console.log(err) })
}

function addProfessor(professorArray) {

  professorArray.forEach(professor => {
    document.getElementById("card-wrapper").innerHTML +=
      `
    <div class="card swiper-slide">
    <div class="content">
      <div class="front">
        <div class="image-content">
          <span class="overlay"></span>
          <div class="card-image">
            <img src="./img/avatar.jpg" alt="" class="card-img">
          </div>
        </div>
        <div class="card-content">
          <h2 class="name">${professor.first_name} ${professor.last_name}</h2>
          <button class="button-card" onclick="flipCard(this),fetchSubject(${professor.id})">Vezi Cursuri</button>
        </div>
      </div>
      <div class="back">

        <h1 class="title-curs">Cursuri:</h1>
        <ul class="courses-list" id="professor-id${professor.id}">

        </ul>
        <button class="button-card back-button" onclick="flipCard(this)">Înapoi</button>
      </div>
    </div>
  </div>
`
  })
}
function addSubjects(subjectsArray, id) {
  const coursesList = document.getElementById(`professor-id${id}`);

  if (coursesList.children.length === 0) {
    subjectsArray.forEach(subject => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      const button = document.createElement('button');

      a.href = './infoCurs.html';
      button.className = 'button-courses';
      button.role = 'button';
      button.textContent = subject.abbreviation;

      a.appendChild(button);
      li.appendChild(a);
      coursesList.appendChild(li);

    });
  }
}


document.addEventListener("DOMContentLoaded", function () {
  fetchProfessor();
});