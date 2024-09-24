"use client";
import { useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";


interface ProfessorCardProps {
  professorID: number;
  firstName: string;
  lastName: string;
  gender: "male" | "female";
  avgRating: number;
}

interface ProfessorSubjects {
  courses: string[];
  laboratories: string[];
  seminars: string[];
  projects: string[];
}

export default function ProfessorCard({
  professorID,
  firstName,
  lastName,
  gender,
}: ProfessorCardProps) {
  const defaultImageSrc =
    gender === "male"
      ? `/svg/professors/npc-male.svg`
      : `/svg/professors/npc-female.svg`;

  const [imageSrc, setImageSrc] = useState(
    `/svg/professors/${lastName.toLowerCase()}.svg`
  );

  return (
    <>
      <div className={styles.cardContainer}>
        <div className={styles.avatarContainer}>
          <Image
            width={80}
            height={80}
            src={imageSrc}
            alt="Professor Avatar"
            className={styles.professorAvatar}
            onError={() => setImageSrc(defaultImageSrc)}
          />
        </div>
        <div className={styles.infoContainer}>
          <h1>
            {lastName} {firstName}
          </h1>
          <Link
            href={{
              pathname: `/panel/${professorID}`,
            }}
            className={styles.arrowLink}
          >
            <Image
              height={40}
              width={40}
              alt="Arrow symbol"
              src={"/svg/arrow-forward.svg"}
              className={styles.arrowButton}
            />
          </Link>
        </div>
      </div>
    </>

  
  );
}
