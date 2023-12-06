'use client'

import Chart from "@/components/infoCourseComponents/Chart";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import RatingOverview from "@/components/infoCourseComponents/RatingOverview";

import { useSearchParams } from 'next/navigation'

export default function InfoCourse() {
  const searchParams = useSearchParams()

  const subjectId = searchParams.get('subjectId')
  return (
    <>

      <div className="info-course-container">

        <Chart subjectId={subjectId} />
        <div className="cont">
          <RatingOverview subjectId={subjectId} />
          <div className="fake-container"></div>
        </div>
      </div>

    </>
  )
}