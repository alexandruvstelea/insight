import React from "react";
import styles from "./loadingSpin.module.css";
import Footer from "../footer/Footer";
import Header from "../header/Header";

export default function Loading() {
  return (
    <>
      <div className={styles.loadingPageContainer}>
        <Header />
        <div className={styles.spinner}>
          <div className={styles.loader}></div>
        </div>
        <Footer />
      </div>
    </>
  );
}
