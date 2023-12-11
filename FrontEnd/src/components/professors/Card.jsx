'use client'
import Image from 'next/image'
import React, { useState } from 'react';
import Subject from './Subject';
import styles from './card.module.css'
export default function Card({ professor }) {

  const [isFlipped, setIsFlipped] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);


  async function fetchSubject(professor_id) {
    if (!isLoaded) {
      const url = `${process.env.REACT_APP_API_URL}/subjects/professor/${professor_id}`;
      try {
        const response = await fetch(url);
        const complete_response = await response.json();
        setSubjects(complete_response);
        setIsLoaded(true);
      } catch (err) {
        console.log(err);
      }
    }
  }

  const flipCard = () => {
    setIsFlipped(!isFlipped);
    if (!isFlipped) {
      fetchSubject(professor.id);
    }
  };


  return (
    <>
      <div className={`${styles.card} ${isFlipped ? styles.flipped : ''}`}>
        <div className={styles.content}>
          <div className={styles.front}>
            <div className={styles.imageContent}>
              <span className={styles.overlay}></span>
              <div className={styles.cardImage}>
                <Image
                  width={158}
                  height={158}
                  src={professor.gender === 'male' ? "/images/maleAvatar4.png" : "/images/femaleAvatar4.png"}
                  alt="Avatar"
                  className={styles.cardImg} />
              </div>
            </div>
            <div className={styles.cardContent}>
              <h2 className={styles.name}>{professor.first_name} {professor.last_name}</h2>
              <button className={styles.buttonCard} onClick={flipCard}>Vezi Cursuri</button>
            </div>
          </div>
          <div className={styles.back}>

            <h1 className={styles.titleCurs}>Cursuri:</h1>
            <ul className={styles.coursesList} >
              {isLoaded && subjects.map(subject => (
                <Subject key={subject.id} subject={subject} />
              ))}
            </ul>
            <button className={`${styles.buttonCard} ${styles.backButton}`} onClick={flipCard}>Înapoi</button>
          </div>
        </div>
      </div >
    </>
  )
}