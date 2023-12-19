"use client";
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import Likes from "@/components/infoCourse/Likes";
import Comments from "@/components/infoCourse/Comments";
import { useSearchParams } from "next/navigation";
import styles from "./page.module.css";
import React, { useEffect, useState } from "react";

import 'react-toastify/dist/ReactToastify.css';


export default function InfoCourse() {
  const [isError404, setIsError404] = useState(false);
  const searchParams = useSearchParams();
  const subjectId = searchParams.get("subjectId");

  const handleError = (error) => {
    if (error) {
      setIsError404(true);
    }
  };




  return (
    <>

      {isError404 ? (
        <div className={styles.noFoundContainer}>NU EXISTĂ DATE!</div>
      ) : (
        <>
          {/* <div className={styles.infoCourseContainer}>
            <Chart onError={handleError} subjectId={subjectId} />
            <div className={styles.container}>
              <RatingOverview subjectId={subjectId} onError={handleError} />
              { <LikeDislike subjectId={subjectId} /> }
            </div>
            <div className={styles.containerComments}>
              <Comments subjectId={subjectId} />
            </div >
          </div > */}
          <div className={styles.gridContainer}>
            <div className={styles.gridItem1}>
              <Chart onError={handleError} subjectId={subjectId} />
            </div>
            <div className={styles.container}>
              <div className={styles.gridItem2}>
                <RatingOverview subjectId={subjectId} onError={handleError} />
                <Likes subjectId={subjectId} />
              </div>
            </div>
            <div className={styles.gridItem3}>
              <Comments subjectId={subjectId} />
            </div>
          </div>
        </>
      )
      }

    </>
  );
}
