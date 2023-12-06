'use client'
import { useState, useEffect } from 'react'
import { Navigation, Pagination, A11y } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import Card from './Card';
import { Scale } from 'chart.js';

export default function CustomSlider() {
  const [professors, setProfessors] = useState([]);

  useEffect(() => {
    fetchProfessors();
  }, []);


  async function fetchProfessors() {
    const url = `http://127.0.0.1:5000/professors`;
    try {
      const response = await fetch(url, { method: "GET" });
      const complete_response = await response.json();
      setProfessors(complete_response);
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <div className='swiper-container'>
      <Swiper

        modules={[Navigation, Pagination, A11y]}
        speed={500}
        pagination={{
          dynamicBullets: true,
          clickable: true,
        }}
        navigation={{
          navigation: true,
        }}
        breakpoints={{
          0: {
            slidesPerView: 1,
            slidesPerGroup: 1,
          },
          580: {
            slidesPerView: 2,
            slidesPerGroup: 2,
          },
          990: {
            slidesPerView: 3,
            slidesPerGroup: 3,
          },
          1300: {
            slidesPerView: 4,
            slidesPerGroup: 4,
          },
          1600: {
            slidesPerView: 5,
            slidesPerGroup: 5,
          },
        }}
      >
        <div className='swiper-container'>
          {professors.map((professor, index) => (

            < SwiperSlide key={index} >
              <div className="card-container">
                <Card professor={professor} />
              </div>
            </SwiperSlide>
          ))}
        </div>
      </Swiper >
    </div >
  )
}