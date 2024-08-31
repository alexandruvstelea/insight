"use client";
import styles from "./page.module.css";
import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

interface ProfessorCard {
  professorID: number;
  firstName: string;
  lastName: string;
  gender: string;
}

export default function ProfessorCard({
  professorID,
  firstName,
  lastName,
  gender,
}: ProfessorCard) {
  const avatarPath =
    gender === "male" ? `/png/maleAvatar.png` : "/png/femaleAvatar.png";
  const [isFlipped, setIsFlipped] = useState(false);
  const flipCard = () => {
    setIsFlipped(!isFlipped);
  };
  return (
    <>
      <div className={`${styles.card} ${isFlipped ? styles.flipped : ""}`}>
        <div className={styles.content}>
          <div className={styles.front}>
            <div className={styles.imageContent}>
              <div className={styles.cardImage}>
                <Image
                  width={128}
                  height={128}
                  src={avatarPath}
                  alt="Avatar"
                  className={styles.professorAvatar}
                />
              </div>
            </div>
            <div className={styles.cardContent}>
              <h2 className={styles.name}>
                {firstName} {lastName}
              </h2>

              <button className={styles.buttonCard} onClick={flipCard}>
                Vezi Cursuri
              </button>
            </div>
          </div>
          <div className={styles.back}>
            <button
              className={`${styles.buttonCard} ${styles.backButton}`}
              onClick={flipCard}
            >
              &#206;napoi
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
