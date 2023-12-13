'use client'
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import LikeDislike from "@/components/infoCourse/LikeDislike";
import { useSearchParams } from 'next/navigation'
import styles from './page.module.css'
import React, { useState } from 'react';

export default function InfoCourse() {
  const [isError404, setIsError404] = useState(false);
  const searchParams = useSearchParams()
  const subjectId = searchParams.get('subjectId')

  const handleError = (error) => {
    if (error) {
      setIsError404(true);
    }
  };


  return (
    <>
      {isError404 ? <div className={styles.noFoundContainer}>NU EXISTĂ DATE!</div> : (
        <div className={styles.infoCourseContainer}>

          <Chart onError={handleError} subjectId={subjectId} />
          <div className={styles.container}>
            <RatingOverview subjectId={subjectId} onError={handleError} />
            <LikeDislike subjectId={subjectId} />
          </div>
        </div>
      )
      }
    </>
  )
}