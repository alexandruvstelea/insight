"use client";
import styles from "./page.module.css";
import { useState, useEffect } from "react";
import Image from "next/image";
import { fetchSubjectsByProfessor } from "@/utils/fetchers/subjects";

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
  avgRating,
}: ProfessorCardProps) {
  const [subjects, setSubjects] = useState<ProfessorSubjects>({
    courses: [],
    laboratories: [],
    seminars: [],
    projects: [],
  });
  const [isFlipped, setIsFlipped] = useState(false);
  const avatarPath =
    gender === "male" ? "/png/maleAvatar.png" : "/png/femaleAvatar.png";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedSubjects: any = await fetchSubjectsByProfessor(
          professorID
        );
        setSubjects(fetchedSubjects);
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    };

    fetchData();
  }, [professorID]);

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
          <div className={styles.professorSubjects}>
            {subjects.courses && subjects.courses.length > 0 ? (
              <div className={styles.professorCourses}>
                <h1>Cursuri</h1>
                {subjects.courses.map((course: string, index: number) => (
                  <h2 key={index}>{course}</h2>
                ))}
              </div>
            ) : null}
            {subjects.laboratories && subjects.laboratories.length > 0 ? (
              <div className={styles.professorLaboratories}>
                <h1>Laboratoare</h1>
                {subjects.laboratories.map(
                  (laboratory: string, index: number) => (
                    <h2 key={index}>{laboratory}</h2>
                  )
                )}
              </div>
            ) : null}
            {subjects.seminars && subjects.seminars.length > 0 ? (
              <div className={styles.professorSeminars}>
                <h1>Seminare</h1>
                {subjects.seminars.map((seminar: string, index: number) => (
                  <h2 key={index}>{seminar}</h2>
                ))}
              </div>
            ) : null}
            {subjects.projects && subjects.projects.length > 0 ? (
              <div className={styles.professorLaboratories}>
                <h1>Proiecte</h1>
                {subjects.projects.map((project: string, index: number) => (
                  <h2 key={index}>{project}</h2>
                ))}
              </div>
            ) : null}
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
