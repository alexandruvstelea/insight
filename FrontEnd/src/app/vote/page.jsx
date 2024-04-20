"use client";
import React, { useState, useEffect } from "react";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import styles from "./page.module.css";
import PropTypes from "prop-types";
import { styled } from "@mui/material/styles";
import Rating from "@mui/material/Rating";
import SentimentVeryDissatisfiedIcon from "@mui/icons-material/SentimentVeryDissatisfied";
import SentimentDissatisfiedIcon from "@mui/icons-material/SentimentDissatisfied";
import SentimentSatisfiedIcon from "@mui/icons-material/SentimentSatisfied";
import SentimentSatisfiedAltIcon from "@mui/icons-material/SentimentSatisfiedAltOutlined";
import SentimentVerySatisfiedIcon from "@mui/icons-material/SentimentVerySatisfied";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { useSearchParams } from "next/navigation";
import { extractTextFromHTML } from "@/app/Actions/functions";
import { useRouter } from "next/navigation";
import { fetchCheckLogin } from "@/app/Actions/getUserData";
export default function Vote() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [roomId, setRoomId] = useState(null);

  useEffect(() => {
    const roomIdParam = searchParams.get("roomId");
    if (roomIdParam) {
      setRoomId(roomIdParam);
    }
  }, []);

  useEffect(() => {
    const checkLoggedIn = async () => {
      try {
        const user = await fetchCheckLogin();
        if (!user.logged_in) {
          const roomIdParam = searchParams.get("roomId");
          if (roomIdParam) {
            sessionStorage.setItem("roomId", roomIdParam);
          }
          router.push("/login");
        }
      } catch (error) {
        console.error("Error checking login status:", error);
      }
    };

    checkLoggedIn();
  }, []);

  useEffect(() => {
    const roomIdFromStorage = sessionStorage.getItem("roomId");
    if (roomIdFromStorage) {
      setRoomId(roomIdFromStorage);
      sessionStorage.removeItem("roomId");
    }
  }, []);

  const [errorMessage, setErrorMessage] = useState("");
  const [comment, setComment] = useState("");
  const [code, setCode] = useState("");
  const [showPopup, setShowPopup] = useState(false);
  const [redirectCountdown, setRedirectCountdown] = useState(5);

  useEffect(() => {
    let countdownInterval;

    if (showPopup) {
      countdownInterval = setInterval(() => {
        setRedirectCountdown((prevCountdown) => prevCountdown - 1);
      }, 1000);
    }

    return () => clearInterval(countdownInterval);
  }, [showPopup]);

  useEffect(() => {
    if (redirectCountdown === 0) {
      router.push("/");
    }
  }, [redirectCountdown]);

  const StyledRating = styled(Rating)(({ theme }) => ({
    "& .MuiRating-iconEmpty .MuiSvgIcon-root": {
      color: theme.palette.action.disabled,
      fontSize: "50px",
    },
    "& .MuiRating-iconFilled .MuiSvgIcon-root": {
      fontSize: "50px",
    },
  }));
  const [ratings, setRatings] = useState({
    clarity: null,
    comprehension: null,
    interactivity: null,
    relevance: null,
  });
  const handleRatingChange = (name, value) => {
    setRatings({
      ...ratings,
      [name]: value,
    });
  };
  const handleSubmit = async () => {
    if (
      ratings.clarity === null ||
      ratings.comprehension === null ||
      ratings.interactivity === null ||
      ratings.relevance === null
    ) {
      setErrorMessage("Te rugăm să evaluezi toate categoriile.");
      return;
    } else if (code.length !== 6) {
      setErrorMessage("Codul este incorect.");
      return;
    } else if (comment.length !== 0 || comment.length >= 20) {
      setErrorMessage(
        "Comentariul trebuie să contină între 1 și 20 de caractere."
      );
      return;
    } else {
      setErrorMessage("");
    }

    const currentDateTime = new Date();
    const year = currentDateTime.getFullYear();
    const month = String(currentDateTime.getMonth() + 1).padStart(2, "0");
    const day = String(currentDateTime.getDate()).padStart(2, "0");
    const hours = String(currentDateTime.getHours()).padStart(2, "0");
    const minutes = String(currentDateTime.getMinutes()).padStart(2, "0");
    const seconds = String(currentDateTime.getSeconds()).padStart(2, "0");
    const milliseconds = String(currentDateTime.getMilliseconds()).padStart(
      3,
      "0"
    );
    const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;

    const ratingsFormData = new FormData();
    ratingsFormData.append("date", "2024-04-15 09:00:10.559345"); // for testing purposes
    // ratingsFormData.append("date", formattedDateTime);
    ratingsFormData.append("clarity", ratings.clarity);
    ratingsFormData.append("interactivity", ratings.interactivity);
    ratingsFormData.append("relevance", ratings.relevance);
    ratingsFormData.append("comprehension", ratings.comprehension);
    ratingsFormData.append("code", code);
    ratingsFormData.append("room_id", roomId);

    const commentsFormData = new FormData();
    commentsFormData.append("comment", comment);
    commentsFormData.append("code", code);
    commentsFormData.append("room_id", roomId);

    if (comment.trim() !== "") {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/comments`,
          {
            method: "POST",
            credentials: "include",
            body: commentsFormData,
          }
        );

        if (response.ok) {
          setErrorMessage("");
        } else if (response.status === 400) {
          const errorMessage = await response.text();
          setErrorMessage(extractTextFromHTML(errorMessage));
          return;
        }
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rating`, {
        method: "POST",
        credentials: "include",
        body: ratingsFormData,
      });

      if (response.ok) {
        setErrorMessage("");
        setShowPopup(true);
      } else if (response.status === 400) {
        const errorMessage = await response.text();
        setErrorMessage(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const customIcons = {
    1: {
      icon: <SentimentVeryDissatisfiedIcon color="error" />,
      label: "Very Dissatisfied",
    },
    2: {
      icon: <SentimentDissatisfiedIcon color="error" />,
      label: "Dissatisfied",
    },
    3: {
      icon: <SentimentSatisfiedIcon color="warning" />,
      label: "Neutral",
    },
    4: {
      icon: <SentimentSatisfiedAltIcon color="success" />,
      label: "Satisfied",
    },
    5: {
      icon: <SentimentVerySatisfiedIcon color="success" />,
      label: "Very Satisfied",
    },
  };

  function IconContainer(props) {
    const { value, ...other } = props;
    return <span {...other}>{customIcons[value].icon}</span>;
  }

  IconContainer.propTypes = {
    value: PropTypes.number.isRequired,
  };

  return (
    <>
      <div className={styles.formPageContainer}>
        <Header />
        <div className={styles.contentContainer}>
          <form className={styles.form}>
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                my: 3,
                width: "350px",
              }}
            >
              <Box sx={{ my: 1 }}>
                <h2 className={styles.titleRating}>Claritate</h2>
                <StyledRating
                  IconContainerComponent={IconContainer}
                  highlightSelectedOnly
                  name="claritate"
                  value={ratings.clarity}
                  onChange={(event, newValue) =>
                    handleRatingChange("clarity", newValue)
                  }
                  size="large"
                />
              </Box>
              <Box sx={{ my: 1 }}>
                <h2 className={styles.titleRating}>Înțelegere</h2>
                <StyledRating
                  IconContainerComponent={IconContainer}
                  highlightSelectedOnly
                  name="intelegere"
                  value={ratings.comprehension}
                  onChange={(event, newValue) =>
                    handleRatingChange("comprehension", newValue)
                  }
                  size="large"
                />
              </Box>
              <Box sx={{ my: 1 }}>
                <h2 className={styles.titleRating}>Interactivitate</h2>
                <StyledRating
                  IconContainerComponent={IconContainer}
                  highlightSelectedOnly
                  name="interactivitate"
                  value={ratings.interactivity}
                  onChange={(event, newValue) =>
                    handleRatingChange("interactivity", newValue)
                  }
                  size="large"
                />
              </Box>
              <Box sx={{ my: 1 }}>
                <h2 className={styles.titleRating}>Relevanţă</h2>
                <StyledRating
                  IconContainerComponent={IconContainer}
                  highlightSelectedOnly
                  name="relevanta"
                  value={ratings.relevance}
                  onChange={(event, newValue) =>
                    handleRatingChange("relevance", newValue)
                  }
                  size="large"
                />
              </Box>

              <div className={styles.commentContainer}>
                <h2 className={styles.titleRating}>Comentarii</h2>
                <textarea
                  className={styles.commentInput}
                  name="comment"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                />
                <p className={styles.optionalText}>
                  * Completarea acestui câmp este opțională.
                </p>
                <p className={styles.optionalText}>
                  * Toate ratingurile sunt anonime.
                </p>
              </div>
              <div className={styles.codeContainer}>
                <h2 className={styles.titleRating}>Cod</h2>
                <input
                  className={styles.codeInput}
                  type="number"
                  name="code"
                  value={code}
                  required
                  onChange={(e) => {
                    const value = e.target.value;
                    const newValue = value.replace(/[^\d]/g, "").slice(0, 6);
                    setCode(newValue);
                  }}
                />
              </div>
              {errorMessage && (
                <div className={styles.errorText}>{errorMessage}</div>
              )}
              <Button
                variant="contained"
                color="primary"
                size="large"
                sx={{
                  padding: "10px 24px",
                  fontSize: "1rem",
                }}
                onClick={handleSubmit}
              >
                Trimite rating-urile
              </Button>
            </Box>
          </form>
          {showPopup && (
            <div className={styles.popupOverlay}>
              <div className={styles.popup}>
                <p>Vă mulțumim!</p>
                <p>Veți fi redirecționat în {redirectCountdown} secunde.</p>

                <div className={styles.progressBar}>
                  <div
                    className={styles.progress}
                    style={{ width: `${(redirectCountdown / 5) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
        <Footer />
      </div>
    </>
  );
}
