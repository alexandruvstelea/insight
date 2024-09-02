"use client";
// import { Navigation } from "swiper/modules";
// import { Swiper, SwiperSlide } from "swiper/react";
// import "swiper/css";
// import "swiper/css/navigation";
import ProfessorCard from "../professorCard/page";
import styles from "./page.module.css";

interface ProfessorsSlider {
  professors: any;
}

export default function ProfessorsSlider({ professors }: ProfessorsSlider) {
  //   const swiperSettings = {
  //     modules: [Navigation],
  //     speed: 500,
  //     slidesPerView: 4,
  //     navigation: true,
  //     breakpoints: {
  //       0: {
  //         slidesPerView: 1,
  //         slidesPerGroup: 1,
  //       },
  //       850: {
  //         slidesPerView: 2,
  //         slidesPerGroup: 2,
  //       },
  //       1350: {
  //         slidesPerView: 3,
  //         slidesPerGroup: 3,
  //       },
  //       1700: {
  //         slidesPerView: 4,
  //         slidesPerGroup: 4,
  //       },
  //     },
  //   };

  return (
    <>
      {/* <Swiper {...swiperSettings}>
        {professors.map((professor: any) => (
          <SwiperSlide key={professor.id}> */}
      <div className={styles.cardContainer}>
        <ProfessorCard
          professorID={professors[0].id}
          firstName={professors[0].first_name}
          lastName={professors[0].last_name}
          gender={professors[0].gender}
          avgRating={professors[0].avgRating}
        />
      </div>
      {/* </SwiperSlide>
        ))}
      </Swiper> */}
    </>
  );
}
