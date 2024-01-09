import styles from './loadingSpin.module.css'
import React from "react";
import Image from "next/image";

export default function Loading() {

  return (
    <div className={styles.spinner}>
      <div className={styles.loader}></div>
      <img src={"/images/unitbvLogo.png"} alt="Loading" className={styles.image} />
    </div>
  )
}