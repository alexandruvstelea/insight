
import styles from "./page.module.css";
import React from "react";
import Image from "next/image";
export default function Loading() {
  return (
    <div className={styles.spinner}>
      <div className={styles.loader}></div>
      <Image width={100} height={100} src={"/images/unitbvLogo.png"} alt="Loading" className={styles.image} />
    </div>
  )
}