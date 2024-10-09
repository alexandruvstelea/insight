"use client";
import styles from "./page.module.css";
import React, { useState } from "react";
import { SubjectWithAssociation } from "@/utils/fetchers/subjects";
import Link from "next/link";

interface SubjectDropdownProps {
  subject: SubjectWithAssociation;
  facultyId: number;
  professorId: number;
}

export default function SubjectDropdown({
  subject,
  facultyId,
  professorId,
}: SubjectDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen((prev) => !prev);
  };

  return (
    <div className={styles.dropdown}>
      <button className={styles.dropdownButton} onClick={toggleDropdown}>
        {subject.name}
      </button>

      <div className={`${styles.dropdownMenu} ${isOpen ? styles.open : ""}`}>
        {subject.isCourse && (
          <Link
            href={{
              pathname: `/panel/${facultyId}/${professorId}/course/${subject.id}`,
            }}
            className={styles.dropdownLink}
          >
            <button className={styles.dropdownItem}>Curs</button>
          </Link>
        )}
        {subject.isLaboratory && (
          <Link
            href={{
              pathname: `/panel/${facultyId}/${professorId}/laboratory/${subject.id}`,
            }}
            className={styles.dropdownLink}
          >
            <button className={styles.dropdownItem}>Laborator</button>
          </Link>
        )}
        {subject.isSeminar && (
          <Link
            href={{
              pathname: `/panel/${facultyId}/${professorId}/seminar/${subject.id}`,
            }}
            className={styles.dropdownLink}
          >
            <button className={styles.dropdownItem}>Seminar</button>
          </Link>
        )}
        {subject.isProject && (
          <Link
            href={{
              pathname: `/panel/${facultyId}/${professorId}/project/${subject.id}`,
            }}
            className={styles.dropdownLink}
          >
            <button className={styles.dropdownItem}>Proiect</button>
          </Link>
        )}
      </div>
    </div>
  );
}
