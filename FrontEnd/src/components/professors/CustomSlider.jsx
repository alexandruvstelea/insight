'use client'
import { useState, useEffect } from 'react'
import { Navigation, Pagination, A11y } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import styles from './customSlider.module.css'
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import Card from './Card';

export default function CustomSlider({ searchTerm, onError }) {
  const [professors, setProfessors] = useState([]);
  const [error404, setError404] = useState(false);
  const filteredProfessors = professors.filter(professor =>
    `${professor.first_name} ${professor.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
  );


  useEffect(() => {
    fetchProfessors();
  }, []);



  async function fetchProfessors() {
    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/professors` }
    else { url = `${process.env.REACT_APP_API_URL}/professors_archive/${selectedYear}` }
    try {
      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        if (response.status === 404) {
          setError404(true);
        }
        throw new Error(`HTTP error: ${response.status}`);
      }

      const complete_response = await response.json();
      setProfessors(complete_response);
    } catch (err) {
      console.log(err);
    }
  }

  const swiperSettings = {
    modules: [Navigation, Pagination, A11y],
    speed: 500,
    slidesPerView: 5,
    pagination: {
      dynamicBullets: true,
      clickable: true,
    },
    navigation: {
      navigation: true,
    },

    breakpoints: {
      0: {
        slidesPerView: 1,
        slidesPerGroup: 1,
      },
      677: {
        slidesPerView: 2,
        slidesPerGroup: 2,
      },
      1030: {
        slidesPerView: 3,
        slidesPerGroup: 3,
      },
      1350: {
        slidesPerView: 4,
        slidesPerGroup: 4,
      },
      1700: {
        slidesPerView: 5,
        slidesPerGroup: 5,
      },
    }
  }

  useEffect(() => {
    if (error404) {
      onError(true);
    }
  }, [error404]);

  return (
    <div>

      <Swiper {...swiperSettings}>
        {filteredProfessors.map((professor, index) => (
          < SwiperSlide key={professor.id} >
            <div className={styles.cardContainer}>
              <Card professor={professor} />
            </div>
          </SwiperSlide>
        ))}
      </Swiper >
    </div >
  )
}
