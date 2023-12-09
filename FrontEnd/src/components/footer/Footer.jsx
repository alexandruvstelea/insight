import Image from 'next/image'
import Link from "next/link";
import styles from './footer.module.css'
export default function Footer() {
  return (
    <>
      <div className={styles.copyRight}>
        <div className={styles.copyRightContent}>
          <i className="fa-solid fa-copyright"></i>
          © Developed by
          <a href="https://www.linkedin.com/in/cristianandreisava" target="_blank" rel="noopener noreferrer">Sava Andrei</a>
          and
          <a href="https://www.linkedin.com/in/alexandrustelea" target="_blank" rel="noopener noreferrer">Stelea Alexandru</a>
        </div>
        <div className={styles.copyRightAdminLogo}>
          <Link href="/adminLogin"><Image width={27} height={27} src="/images/adminLogo.png" alt="ADMIN" /></Link>
        </div>
      </div>
    </>
  )
}