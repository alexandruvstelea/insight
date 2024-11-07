"use client";
import React, { useState, useEffect, useRef } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import { sendIssueReport } from "@/utils/fetchers/reports";
import { send } from "process";

export default function IssueReport() {
  const [isOpen, setIsOpen] = useState(false);
  const [problemText, setProblemText] = useState("");
  const popupRef = useRef<HTMLDivElement>(null);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  const handleClose = () => {
    setIsOpen(false);
    setProblemText("");
  };

  const handleSubmit = async () => {
    await sendIssueReport(problemText);
    setProblemText("");
    handleClose();
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
      handleClose();
    }
  };

  useEffect(() => {
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <>
      <div className={styles.flagContainer}>
        <Image
          src="/svg/flag.svg"
          width={24}
          height={24}
          alt="Report Flag"
          className={styles.reportFlag}
          onClick={handleOpen}
        />
      </div>
      {isOpen && (
        <div className={styles.popUp} ref={popupRef}>
          <h3>Raportează o problemă</h3>
          <textarea
            className={styles.textArea}
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            rows={4}
            placeholder="Descrie problema întâlnită"
          />
          <button onClick={handleSubmit} className={styles.submitButton}>
            Trimite
          </button>
          <button className={styles.closeButton} onClick={handleClose}>
            Anulează
          </button>
        </div>
      )}
    </>
  );
}
