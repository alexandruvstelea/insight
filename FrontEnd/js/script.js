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
    <div class="card swiper-slide">

            <div class="image-content">
                <span class="overlay"></span>

                <div class="card-image">
                    <img src="./img/avatar.jpg" alt="" class="card-img">
                </div>
            </div>

            <div class="card-content">
                <h2 class="name">Nume profesor</h2>
                <p class="description">${elem}</p>

                <button class="button" id="card-button" >Vezi Cursuri</button>
            </div>
        </div>
    
`
}

