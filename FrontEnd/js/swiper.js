var swiper = new Swiper(".slide-container", {
  slidesPerView: 5, 
  slidesPerGroup: 5, 
  spaceBetween: 25,
  loop: false,
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

const flipCard = (button) => button.closest('.card').classList.toggle('flipped');
