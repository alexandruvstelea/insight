"use client";
import { useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";
import { transformProfessorName } from "@/utils/fetchers/professors";

interface ProfessorCardProps {
  professorID: number;
  firstName: string;
  lastName: string;
  gender: "male" | "female";
  facultyAbbreviation: string;
}

export default function ProfessorCard({
  professorID,
  firstName,
  lastName,
  gender,
  facultyAbbreviation,
}: ProfessorCardProps) {
  const defaultImageSrc =
    gender === "male"
      ? `/svg/professors/npc-male.svg`
      : `/svg/professors/npc-female.svg`;

  const removeDiacritics = (str: string) => {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  };

  const [imageSrc, setImageSrc] = useState(
    `/svg/professors/${removeDiacritics(lastName.toLowerCase())}.svg`
  );

  const professorName: string = transformProfessorName(lastName, firstName);

  return (
    <>
      <Link
        href={{
          pathname: `/feedback/${facultyAbbreviation}/${professorName}`,
        }}
        className={styles.cardLink}
      >
        <div className={styles.cardContainer}>
          <div className={styles.avatarContainer}>
            <Image
              width={80}
              height={80}
              src={imageSrc}
              alt="Professor Avatar"
              className={styles.professorAvatar}
              onError={() => setImageSrc(defaultImageSrc)}
            />
          </div>
          <div className={styles.infoContainer}>
            <h1>
              {lastName} {firstName}
            </h1>

            <Image
              height={40}
              width={40}
              alt="Arrow symbol"
              src={"/svg/arrow-forward.svg"}
              className={styles.arrowButton}
            />
          </div>
        </div>
      </Link>
    </>
  );
}
