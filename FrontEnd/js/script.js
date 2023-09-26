var swiper = new Swiper(".slide-content", {
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
  allowTouchMove: false,
  breakpoints: {
    0: {
      slidesPerView: 1,
      slidesPerGroup: 1,
    },
    320: {
      slidesPerView: 2,
      slidesPerGroup: 2,
    },
    640: {
      slidesPerView: 3,
      slidesPerGroup: 3,
    },
    960: {
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

for (let elem = 0; elem < 20; elem++) {
  addProfs(elem)
}

function addProfs(elem) {
  document.getElementById("card-wrapper").innerHTML +=
    `
    <div class="card swiper-slide ">
    <div class="card-inner"> 
    <div class="card-front"> 
      <div class="image-content">
        <span class="overlay"></span>

        <div class="card-image">
          <img src="./img/avatar.jpg" alt="" class="card-img">
        </div>
      </div>

      <div class="card-content">
        <h2 class="name">Nume profesor</h2>
        <p class="description">${elem}</p>
        <button class="button" onclick="flipCard(this)">Vezi Cursuri</button>
        
      </div>
    </div>
    <div class="card-back">
    
      <h1  class="title-curs">Cursuri:</h1>
      <ul class="courses-list">
        <li><a href="./infoCurs.html"<button class="button-30" role="button">AOC</button></a></li>
        <li><a href="./infoCurs.html"<button class="button-30" role="button">IA</button></a></li>
        <li><a href="./infoCurs.html"<button class="button-30" role="button">Econ</button></a></li>
        <li><a href="./infoCurs.html"<button class="button-30" role="button">MS</button></a></li>

      </ul>
      <button class="button back-button" onclick="flipCard(this)">Înapoi</button>
    </div>
  </div>
        </div>
    
`
}


  function flipCard(button) {
    var card = button.closest('.card');
    card.classList.toggle('flipped');
}