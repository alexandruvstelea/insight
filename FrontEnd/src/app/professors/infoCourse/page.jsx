'use client'
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import { useSearchParams } from 'next/navigation'
import styles from './page.module.css'

export default function InfoCourse() {

  const searchParams = useSearchParams()

  const subjectId = searchParams.get('subjectId')
  return (
    <>

      <div className={styles.infoCourseContainer}>

        <Chart subjectId={subjectId} />
        <div className={styles.cont}>
          <RatingOverview subjectId={subjectId} />
          <div className={styles.fakeContainer}></div>
        </div>
      </div>

    </>
  )
}