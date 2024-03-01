"use client";
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";
import Likes from "@/components/infoCourse/Likes";
import Comments from "@/components/infoCourse/Comments";
import DisplayComments from "@/components/infoCourse/DisplayComments";
import { useSearchParams } from "next/navigation";
import styles from "./page.module.css";
import React, { useEffect, useState } from "react";
import LinearProgress from "@mui/material/LinearProgress";
import "react-toastify/dist/ReactToastify.css";
import DropdownArchive from "@/components/header/DropdownArchive";
import Link from "next/link";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";

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
    let url = "";
    if (selectedYear == adjustedYear) {
      url = `${process.env.REACT_APP_API_URL}/nr_likes/${subjectId}`;
    } else {
      url = `${process.env.REACT_APP_API_URL}/nr_likes_archive/${selectedYear}/${subjectId}`;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
      setLikesData(data);
    } catch (err) {
      console.error("Fetch error:", err);
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
    let url = "";
    if (selectedYear == adjustedYear) {
      url = `${process.env.REACT_APP_API_URL}/comments/${subjectId}`;
    } else {
      url = `${process.env.REACT_APP_API_URL}/comments_archive/${selectedYear}/${subjectId}`;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
      setComments(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const fetchApproval = async () => {
    const selectedYear = sessionStorage.getItem("selectedYear");
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;
    let url = "";
    if (selectedYear == adjustedYear) {
      url = `${process.env.REACT_APP_API_URL}/subjects/sentiment/${subjectId}`;
    } else {
      url = `${process.env.REACT_APP_API_URL}/subjects_archive/sentiment/${selectedYear}/${subjectId}`;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
      setApproval(data);
      console.log(data);
    } catch (err) {
      console.error("Fetch error:", err);
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
    fetchApproval();
  }, [subjectId]);

  return (
    <>
      {isError404 ? (
        <div className={styles.cont}>
          <Header />
          <div className={styles.notFoundContainer}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              className={styles.infoSVG}
            >
              <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z" />
            </svg>
            NU EXISTĂ DATE!
          </div>
          <Footer />
        </div>
      ) : (
        <>
          <div className={styles.mainContainer}>
            <div className={styles.header}>
              <div className={styles.headerLeft}>
                <DropdownArchive />
              </div>
              <div className={styles.headerCenter}>
                <h1 className={styles.headerTitle}>
                  <Link href="../professors">FEEDBACK IESC</Link>
                </h1>
              </div>
              <div className={styles.headerRight}>
                <Link href="/adminLogin">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 640 512"
                    className={styles.adminSVG}
                  >
                    <path d="M224 0a128 128 0 1 1 0 256A128 128 0 1 1 224 0zM178.3 304h91.4c11.8 0 23.4 1.2 34.5 3.3c-2.1 18.5 7.4 35.6 21.8 44.8c-16.6 10.6-26.7 31.6-20 53.3c4 12.9 9.4 25.5 16.4 37.6s15.2 23.1 24.4 33c15.7 16.9 39.6 18.4 57.2 8.7v.9c0 9.2 2.7 18.5 7.9 26.3H29.7C13.3 512 0 498.7 0 482.3C0 383.8 79.8 304 178.3 304zM436 218.2c0-7 4.5-13.3 11.3-14.8c10.5-2.4 21.5-3.7 32.7-3.7s22.2 1.3 32.7 3.7c6.8 1.5 11.3 7.8 11.3 14.8v17.7c0 7.8 4.8 14.8 11.6 18.7c6.8 3.9 15.1 4.5 21.8 .6l13.8-7.9c6.1-3.5 13.7-2.7 18.5 2.4c7.6 8.1 14.3 17.2 20.1 27.2s10.3 20.4 13.5 31c2.1 6.7-1.1 13.7-7.2 17.2l-14.4 8.3c-6.5 3.7-10 10.9-10 18.4s3.5 14.7 10 18.4l14.4 8.3c6.1 3.5 9.2 10.5 7.2 17.2c-3.3 10.6-7.8 21-13.5 31s-12.5 19.1-20.1 27.2c-4.8 5.1-12.5 5.9-18.5 2.4l-13.8-7.9c-6.7-3.9-15.1-3.3-21.8 .6c-6.8 3.9-11.6 10.9-11.6 18.7v17.7c0 7-4.5 13.3-11.3 14.8c-10.5 2.4-21.5 3.7-32.7 3.7s-22.2-1.3-32.7-3.7c-6.8-1.5-11.3-7.8-11.3-14.8V467.8c0-7.9-4.9-14.9-11.7-18.9c-6.8-3.9-15.2-4.5-22-.6l-13.5 7.8c-6.1 3.5-13.7 2.7-18.5-2.4c-7.6-8.1-14.3-17.2-20.1-27.2s-10.3-20.4-13.5-31c-2.1-6.7 1.1-13.7 7.2-17.2l14-8.1c6.5-3.8 10.1-11.1 10.1-18.6s-3.5-14.8-10.1-18.6l-14-8.1c-6.1-3.5-9.2-10.5-7.2-17.2c3.3-10.6 7.7-21 13.5-31s12.5-19.1 20.1-27.2c4.8-5.1 12.4-5.9 18.5-2.4l13.6 7.8c6.8 3.9 15.2 3.3 22-.6c6.9-3.9 11.7-11 11.7-18.9V218.2zm92.1 133.5a48.1 48.1 0 1 0 -96.1 0 48.1 48.1 0 1 0 96.1 0z" />
                  </svg>
                </Link>
              </div>
            </div>
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
                <Comments
                  subjectId={subjectId}
                  fetchComments={fetchComments}
                  fetchLikes={fetchLikes}
                />
              </div>
            )}
            <div className={styles.sentimentTitle}>
              <h1>Indicator de sentiment comentarii</h1>
            </div>

            <div className={styles.sentimentContainer}>
              <h1>{approval.positive}%</h1>
              <LinearProgress
                sx={{
                  width: "500px",
                  height: "15px",
                  backgroundColor: "#FF8989",
                }}
                color="primary"
                variant="determinate"
                value={approval.positive}
              />
              <h1>{approval.negative}%</h1>
            </div>
            <DisplayComments subjectId={subjectId} comments={comments} />
            <div className={styles.footer}>
              <div className={styles.footerAuthors}>
                ©{" "}
                <a
                  href="https://alexandrustelea.com"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Alexandru Stelea
                </a>{" "}
                &{" "}
                <a
                  href="https://www.linkedin.com/in/cristianandreisava"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Andrei Sava
                </a>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}
