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
  const handleSubmit = () => {
    console.log("Rating-uri trimise:", ratings);
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
      <Header />
      <form>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            my: 3,
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
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Trimite rating-urile
          </Button>
        </Box>
      </form>
      <Footer />
    </>
  );
}
