import React from "react";
import styles from "./notFoundC.module.css";
import Footer from "../../footer/Footer";
import Header from "../../header/Header";
import Link from "next/link";

export default function NotFoundC() {
  return (
    <>
      <div className={styles.notFoundPageContainer}>
        <Header showArchive={false} />
        <div className={styles.content}>
          <div class={styles.errorContainer}>
            <h1 className={styles.text}> 404 </h1>
            <p className={styles.paragraph}>
              Oops! The page you&apos;re looking can&apos;t be found.
            </p>
            <Link className={styles.link} href="/">
              Go Back to Home
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}
