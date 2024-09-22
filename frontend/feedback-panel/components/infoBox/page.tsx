"use client";
import Image from "next/image";
import { useState, useEffect } from "react";
import styles from "./page.module.css";

interface infoBox {
  title: string;
  content: string;
  imagePath: string;
  reversable: boolean;
}

export function InfoBox({ title, content, imagePath, reversable }: infoBox) {
  const [canReverse, setCanReverse] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setCanReverse(window.innerWidth >= 1024);
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);
  return (
    <>
      {(!canReverse || !reversable) && (
        <>
          <div className={styles.infoBoxContainer}>
            <div className={styles.infoBox}>
              <h1>{title}</h1>
              <h2>{content}</h2>
            </div>
            <Image
              width={80}
              height={80}
              src={imagePath}
              alt="Landing Page About Image"
              className={styles.decorativeImage}
            />
          </div>
        </>
      )}
      {canReverse && reversable && (
        <>
          <div className={styles.infoBoxContainer}>
            <Image
              width={80}
              height={80}
              src={imagePath}
              alt="Landing Page About Image"
              className={styles.decorativeImage}
            />
            <div className={styles.infoBox}>
              <h1>{title}</h1>
              <h2>{content}</h2>
            </div>
          </div>
        </>
      )}
    </>
  );
}
