"use client";
import styles from "./page.module.css";
import { useState } from "react";
import Image from "next/image";

interface ProfessorCardProps {
  professorID: number;
  firstName: string;
  lastName: string;
  gender: "male" | "female";
  avgRating: number;
}

export default function ProfessorCard({
  firstName,
  lastName,
  gender,
  avgRating,
}: ProfessorCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const avatarPath =
    gender === "male" ? "/png/maleAvatar.png" : "/png/femaleAvatar.png";

  const flipCard = () => setIsFlipped(!isFlipped);

  return (
    <div className={`${styles.card} ${isFlipped ? styles.flipped : ""}`}>
      <div className={styles.cardContent}>
        <div className={styles.front}>
          <div className={styles.cardImageContainer}>
            <div className={styles.cardAvatar}>
              <Image
                width={128}
                height={128}
                src={avatarPath}
                alt="Professor avatar"
                className={styles.professorAvatar}
              />
            </div>
          </div>
          <div className={styles.cardInfo}>
            <h1 className={styles.name}>
              {firstName}&nbsp;{lastName}
            </h1>
            <div className={styles.cardRating}>
              <Image
                src={"/svg/hurricane-solid.svg"}
                width={40}
                height={40}
                alt="Faculty logo"
                className={styles.cardRatingImage}
                quality={100}
              />
              {avgRating ? <h2>avgRating</h2> : <h3>Nu există scor</h3>}
            </div>
            <button className={styles.cardButton} onClick={flipCard}>
              Cursuri
            </button>
          </div>
        </div>
        <div className={styles.back}>
          <div className={styles.professorCourses}>
            <h1>Cursuri</h1>
          </div>
          <div className={styles.professorLaboratories}>
            <h1>Laboratoare</h1>
          </div>
          <button
            className={`${styles.cardButton} ${styles.backButton}`}
            onClick={flipCard}
          >
            &#206;napoi
          </button>
        </div>
      </div>
    </div>
  );
}
