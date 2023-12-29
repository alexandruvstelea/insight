'use client'
import Image from 'next/image'
import React, { useState, useEffect } from 'react';
import Subject from './Subject';
import styles from './card.module.css'
import { Box, Typography } from '@mui/material';
import GradeRoundedIcon from '@mui/icons-material/GradeRounded';

export default function Card({ professor }) {

  const [isFlipped, setIsFlipped] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [average, setAverage] = useState();
  const imagePath = professor.gender === 'male' ? `/images/maleImages/M16.png` : "/images/femaleAvatar4.png";

  async function fetchSubject(professor_id) {
    if (!isLoaded) {
      const selectedYear = sessionStorage.getItem("selectedYear");
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth() + 1;
      const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
      let url = ''
      if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/subjects/professor/${professor_id}` }
      else { url = `${process.env.REACT_APP_API_URL}/subjects_archive/professor/${selectedYear}/${professor_id}` }

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

  async function fetchAvgProfessor(professor_id) {
    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/professors/average/${professor_id}` }
    else { url = `${process.env.REACT_APP_API_URL}/professors_archive/average/${selectedYear}/${professor_id}` }
    try {
      const response = await fetch(url);

      if (!response.ok) {
        if (response.status === 404) {
          setAverage('N/A');
          console.log(average)
        }
        throw new Error(`HTTP error: ${response.status}`);
      }

      const complete_response = await response.json();
      console.log(complete_response)
      setAverage(complete_response.average);
    } catch (err) {
      console.log(err);
    }

  }

  const flipCard = () => {
    setIsFlipped(!isFlipped);
    if (!isFlipped) {
      fetchSubject(professor.id);
    }
  };

  useEffect(() => {
    fetchAvgProfessor(professor.id)
  }, []);

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
                  src={imagePath}
                  alt="Avatar"
                  className={styles.cardImg} />
              </div>
            </div>
            <div className={styles.cardContent}>
              <h2 className={styles.name}>{professor.first_name} {professor.last_name}</h2>
              <Box position="relative" display="inline-flex" alignItems="center" justifyContent="center" >
                <GradeRoundedIcon sx={{ fontSize: 95, color: '#0040C1' }} />
                <Typography variant="caption" component="span" sx={{
                  position: 'absolute',
                  color: 'white',
                  fontSize: '1.1rem',
                  top: '55%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  fontWeight: 600,
                }}>
                  {average}
                </Typography>
              </Box>
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