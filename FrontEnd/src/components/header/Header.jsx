'use client'
import Link from "next/link";
import WavesSVG from "./WavesSVG";
import styles from './header.module.css'
import DropdownArchive from "@/components/infoCourse/DropdownArchive";
export default function Header() {

  return (
    <>

      <div className={styles.header}>
        <div className={styles.innerHeader}>
          <DropdownArchive />
          <h1 className={styles.headerTitle}><Link href="../professors">FeedBack IESC</Link></h1>
        </div>
        <WavesSVG />
      </div></>

  )
}