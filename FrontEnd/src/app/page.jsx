import Link from 'next/link';
import Image from 'next/image'
import styles from './page.module.css'

export default function Home() {
  console.log('2')
  return (
    <>
      <div className={styles.backgroundLandingPage}>
        <div className={styles.titleLandingPageContainer}>
          <div className={styles.titleLandingPage}>
            <Image width={88} height={88} src="/images/unitbvLogo.png" alt="Logo" className={styles.logoLandingPage} />
            <h1 className={styles.textTitleLandingPage}>FeedBack IESC</h1>
          </div>
          <Link className={styles.buttonLandingPage} href="professors">
            <span className={styles.topKey}></span>
            <span className={styles.text}>Explorează</span>
            <span className={styles.bottomKey1}></span>
            <span className={styles.bottomKey2}></span>
          </Link>
        </div>
        <div className={styles.cube}></div>
        <div className={styles.cube}></div>
        <div className={styles.cube}></div>
        <div className={styles.cube}></div>
        <div className={styles.cube}></div>
        <div className={styles.cube}></div>
      </div>
    </>
  )
}
