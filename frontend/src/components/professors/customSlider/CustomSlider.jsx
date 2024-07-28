"use client";
import React from "react";
import styles from "./customSlider.module.css";
import { Navigation, Pagination, A11y } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/a11y";
import Card from "@/components/professors/card/Card";

export default function CustomSlider({
  professors,
  archive = false,
  year = false,
}) {
  const swiperSettings = {
    modules: [Navigation, Pagination, A11y],
    speed: 500,
    slidesPerView: 4,
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
        slidesPerView: 1,
        slidesPerGroup: 1,
      },
      850: {
        slidesPerView: 2,
        slidesPerGroup: 2,
      },
      1350: {
        slidesPerView: 3,
        slidesPerGroup: 3,
      },
      1700: {
        slidesPerView: 4,
        slidesPerGroup: 4,
      },
    },
  };

  return (
    <div className={styles.container}>
      <div className={styles.swiperContainer}>
        <Swiper {...swiperSettings}>
          {professors.map((professor) => (
            <SwiperSlide key={professor.id}>
              <div className={styles.cardContainer}>
                <Card professor={professor} archive={archive} year={year} />
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </div>
  );
}
