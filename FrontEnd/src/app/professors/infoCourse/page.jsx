"use client";
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import Likes from "@/components/infoCourse/Likes";
import Comments from "@/components/infoCourse/Comments";
import DisplayComments from "@/components/infoCourse/DisplayComments";
import { useSearchParams } from "next/navigation";
import styles from "./page.module.css";
import React, { useEffect, useState } from "react";


import 'react-toastify/dist/ReactToastify.css';


export default function InfoCourse() {
  const [isError404, setIsError404] = useState(false);
  const searchParams = useSearchParams();
  const subjectId = searchParams.get("subjectId");
  const [comments, setComments] = useState([]);
  const [likesData, setLikesData] = useState({ like: 0, dislike: 0 });

  const fetchLikes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/nr_likes/${subjectId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setLikesData(data);

    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const handleError = (error) => {
    if (error) {
      setIsError404(true);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/comments`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setComments(data);

    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  useEffect(() => {
    fetchLikes()
    fetchComments()
  }, [subjectId]);



  return (
    <>

      {isError404 ? (
        <div className={styles.noFoundContainer}>NU EXISTĂ DATE!</div>
      ) : (
        <>
          <div className={styles.mainContainer}>
            <div className={styles.containerCol}>
              <div className={styles.chartContainer}>
                <Chart onError={handleError} subjectId={subjectId} />
              </div>
              <div className={styles.containerRow}>
                <RatingOverview subjectId={subjectId} onError={handleError} />
                <Likes likesData={likesData} />
              </div>
            </div>
            <div className={styles.commentsContainer}>
              <Comments subjectId={subjectId} fetchComments={fetchComments} fetchLikes={fetchLikes} />
            </div>
            <DisplayComments subjectId={subjectId} comments={comments} />
          </div>
        </>
      )
      }

    </>
  );
}
