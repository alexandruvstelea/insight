"use client";
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import Likes from "@/components/infoCourse/Likes";
import Comments from "@/components/infoCourse/Comments";
import DisplayComments from "@/components/infoCourse/DisplayComments";
import { useSearchParams } from "next/navigation";
import styles from "./page.module.css";
import React, { useEffect, useState } from "react";
import LinearProgress from '@mui/material/LinearProgress';
import 'react-toastify/dist/ReactToastify.css';

export default function InfoCourse() {
  const [isError404, setIsError404] = useState(false);
  const searchParams = useSearchParams();
  const subjectId = searchParams.get("subjectId");
  const [comments, setComments] = useState([]);
  const [likesData, setLikesData] = useState({ like: 0, dislike: 0 });
  const [approval, setApproval] = useState({ negative: 0, positive: 0 });

  const [selectedYear, setSelectedYear] = useState(null);
  const [adjustedYear, setAdjustedYear] = useState(null);

  const fetchLikes = async () => {

    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/nr_likes/${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/nr_likes_archive/${selectedYear}/${subjectId}` }

    try {
      const response = await fetch(url);
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
    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/comments/${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/comments_archive/${selectedYear}/${subjectId}` }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setComments(data);
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchApproval = async () => {
    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = ''
    if (selectedYear == adjustedYear) { url = `${process.env.REACT_APP_API_URL}/subjects/sentiment/${subjectId}` }
    else { url = `${process.env.REACT_APP_API_URL}/subjects_archive/sentiment/${selectedYear}/${subjectId}` }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setApproval(data);
      console.log(data)

    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  useEffect(() => {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const newAdjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;

    setAdjustedYear(newAdjustedYear);

    const storedSelectedYear = sessionStorage.getItem("selectedYear");
    setSelectedYear(storedSelectedYear || newAdjustedYear.toString());


    fetchLikes();
    fetchComments();
    fetchApproval()
  }, [subjectId]);


  return (
    <>
      {
        isError404 ? (
          <div className={styles.cont} >
            <div className={styles.noFoundContainer}>NU EXISTĂ DATE!</div>
          </div>
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
              {selectedYear == adjustedYear && (
                <div className={styles.commentsContainer}>
                  <Comments subjectId={subjectId} fetchComments={fetchComments} fetchLikes={fetchLikes} />
                </div>
              )}
              <div className={styles.sentimentTitle}>
                <h1>Indicator de sentiment comentarii</h1>
              </div>

              <div className={styles.sentimentContainer}>
                <h1>{approval.positive}%</h1>
                <LinearProgress sx={{ width: '500px', height: '15px', backgroundColor: "#FF8989" }} color="primary"
                  variant="determinate" value={approval.positive} />
                <h1>{approval.negative}%</h1>
              </div>
              < DisplayComments subjectId={subjectId} comments={comments} />
            </div>
          </>
        )
      }

    </>
  );
}
