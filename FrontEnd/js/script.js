var swiper = new Swiper(".slide-container", {
  slidesPerView: 5, 
  slidesPerGroup: 5, 
  spaceBetween: 25,
  loop: true,
  fade: true,
  grabCursor: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    dynamicBullets: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  allowTouchMove: window.innerWidth <= 850, 
  breakpoints: {
    0: {
      slidesPerView: 1,
      slidesPerGroup: 1,
    },
    580: {
      slidesPerView: 2,
      slidesPerGroup: 2,
    },
    800: {
      slidesPerView: 3,
      slidesPerGroup: 3,
    },
    1080: {
      slidesPerView: 4,
      slidesPerGroup: 4,
    },
    1280: {
      slidesPerView: 4,
      slidesPerGroup: 4,
    },
    1600: {
      slidesPerView: 5,
      slidesPerGroup: 5,
    },
  },
});
window.addEventListener('resize', () => {
  swiper.allowTouchMove = window.innerWidth <= 850;
});

var professorArray = [];
var subjectsArray = [];

function fetchProfessor() {
  const url = 'http://127.0.0.1:5000/professors'
  fetch(url,{method:"GET"})
      .then(function(response) {
          return response.json()
      })
      .then(function(complete_response) {
        addProfessor(complete_response)
      })
      .catch((err) => {
          console.log(err)
      })
}


function fetchSubject(professor_id) {
  const url = `http://127.0.0.1:5000/subjects/${professor_id}`

  fetch(url,{method:"GET"})
      .then(function(response) {
          return response.json()
      })
      .then(function(complete_response) {
        addSubjects(complete_response,professor_id)
      })
      .catch((err) => {
          console.log(err)
      })
}

 function addProfessor(professorArray){

  professorArray.forEach(professor => {
    document.getElementById("card-wrapper").innerHTML +=
    `
    <div class="card swiper-slide" data-flipped="false">
    <div class="content">
      <div class="front">
        <div class="image-content">
          <span class="overlay"></span>
          <div class="card-image">
            <img src="./img/avatar.jpg" alt="" class="card-img">
          </div>
        </div>
        <div class="card-content">
          <h2 class="name">${professor.name} ${professor.surname}</h2>
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
function addSubjects(subjectsArray,id){
 
  const coursesList = document.getElementById(`professor-id${id}`);
  coursesList.innerHTML = ''
subjectsArray.forEach(subject => {
  const li = document.createElement('li');
  const a = document.createElement('a');
  const button = document.createElement('button');

  a.href = './infoCurs.html'; 
  button.className = 'button-courses';
  button.role = 'button';
  button.textContent = subject.abbreviation; // Setați textul butonului

  a.appendChild(button); // Adăugați butonul în link
  li.appendChild(a); // Adăugați link-ul în elementul <li>
  coursesList.appendChild(li); // Adăugați elementul <li> în lista <ul>
});

}
/* <li><a href="./infoCurs.html" <button class="button-courses" role="button">AOC
</button></a></li>
<li><a href="./infoCurs.html" <button class="button-courses" role="button">IA</button></a></li>
<li><a href="./infoCurs.html" <button class="button-courses" role="button">Econ</button></a></li>
<li><a href="./infoCurs.html" <button class="button-courses" role="button">MS</button></a></li>
<li><a href="./infoCurs.html" <button class="button-courses" role="button">MS</button></a></li> */


function flipCard(button) {
  var card = button.closest('.card');
  card.classList.toggle('flipped');
}



