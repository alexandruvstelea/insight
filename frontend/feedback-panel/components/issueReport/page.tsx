"use client";
import React, { useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";

export default function IssueReport() {
  const [isOpen, setIsOpen] = useState(false);
  const [problemText, setProblemText] = useState("");

  const handleOpen = () => {
    if (!isOpen) setIsOpen(true);
    else setIsOpen(false);
  };
  const handleClose = () => setIsOpen(false);
  const handleSubmit = () => {
    setProblemText("");
    handleClose();
  };

  return (
    <>
      <Image
        src="/svg/flag.svg"
        width={24}
        height={24}
        alt="Report Flag"
        className={styles.reportFlag}
        onClick={handleOpen}
      />

      {isOpen && (
        <div className={styles.popUp}>
          <h3>Raporteaza o problema</h3>
          <textarea
            className={styles.textArea}
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            rows={4}
            placeholder="Descrie problema intalnita"
          />
          <button onClick={handleSubmit} className={styles.submitButton}>
            Trimite
          </button>
          <button className={styles.closeButton} onClick={handleClose}>
            Anuleaza
          </button>
        </div>
      )}
    </>
  );
}
