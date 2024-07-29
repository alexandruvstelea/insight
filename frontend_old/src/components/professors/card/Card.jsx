"use client";
import React, { useState } from "react";
import styles from "./card.module.css";
import Image from "next/image";
import { Box, Typography } from "@mui/material";
import GradeRoundedIcon from "@mui/icons-material/GradeRounded";
import SubjectsList from "@/components/professors/subjectsList/SubjectsList";

export default function Card({ professor, archive = false, year = false }) {
  const [isFlipped, setIsFlipped] = useState(false);
  const imagePath =
    professor.gender === "male"
      ? `/images/maleAvatar.png`
      : "/images/femaleAvatar.png";

  const flipCard = () => {
    setIsFlipped(!isFlipped);
  };

  return (
    <>
      <div className={`${styles.card} ${isFlipped ? styles.flipped : ""}`}>
        <div className={styles.content}>
          <div className={styles.front}>
            <div className={styles.imageContent}>
              <div className={styles.cardImage}>
                <Image
                  width={158}
                  height={158}
                  src={imagePath}
                  alt="Avatar"
                  className={styles.cardImg}
                />
              </div>
            </div>
            <div className={styles.cardContent}>
              <h2 className={styles.name}>
                {professor.last_name} {professor.first_name}
              </h2>
              <Box
                position="relative"
                display="inline-flex"
                alignItems="center"
                justifyContent="center"
              >
                <GradeRoundedIcon
                  sx={{ fontSize: 128, color: "#0040C1" }}
                  className={styles.gradeStar}
                />
                <Typography
                  variant="caption"
                  component="span"
                  sx={{
                    position: "absolute",
                    color: "white",
                    fontSize: "24px",
                    top: "54%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    fontWeight: 600,
                  }}
                >
                  {professor.average}
                </Typography>
              </Box>
              <button className={styles.buttonCard} onClick={flipCard}>
                Vezi Cursuri
              </button>
            </div>
          </div>
          <div className={styles.back}>
            <SubjectsList
              subjects={professor.subjects}
              first_name={professor.first_name}
              last_name={professor.last_name}
              archive={archive}
              year={year}
            />
            <button
              className={`${styles.buttonCard} ${styles.backButton}`}
              onClick={flipCard}
            >
              &#206;napoi
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
