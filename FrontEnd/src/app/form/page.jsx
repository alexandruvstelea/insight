"use client";
import React, { useState } from "react";
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

export default function RatingForm() {
  const [errorMessage, setErrorMessage] = useState("");
  const [comment, setComment] = useState("");

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
    clarity: 0,
    comprehension: 0,
    interactivity: 0,
    relevance: 0,
  });
  const handleRatingChange = (name, value) => {
    setRatings({
      ...ratings,
      [name]: value,
    });
  };
  const handleSubmit = async () => {
    if (
      ratings.clarity === 0 ||
      ratings.comprehension === 0 ||
      ratings.interactivity === 0 ||
      ratings.relevance === 0
    ) {
      setErrorMessage(
        "Te rugăm să evaluezi toate categoriile înainte de a trimite."
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
    console.log(formattedDateTime);
    const formData = new FormData();
    // formData.append("date", "2024-04-15 09:00:10.559345");
    formData.append("date", formattedDateTime);
    formData.append("clarity", ratings.clarity);
    formData.append("interactivity", ratings.interactivity);
    formData.append("relevance", ratings.relevance);
    formData.append("comprehension", ratings.comprehension);
    formData.append("subject_id", 3);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rating`, {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      console.log("Rating-uri trimise:", ratings);
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
              <Box sx={{ my: 2 }}>
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
              <Box sx={{ my: 2 }}>
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
              <Box sx={{ my: 2 }}>
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
              <Box sx={{ my: 2 }}>
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

              {errorMessage && (
                <div className={styles.errorText}>{errorMessage}</div>
              )}
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
              >
                Trimite rating-urile
              </Button>
            </Box>
          </form>
        </div>
        <Footer />
      </div>
    </>
  );
}
