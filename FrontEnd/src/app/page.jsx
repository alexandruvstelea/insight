import Link from 'next/link';
import Image from 'next/image'

export default function Home() {
  return (
    <div className="background-landing-page">
      <div className="title-landing-page-container">
        <div className="title-landing-page">
          <Image width={88} height={88} src="/images/unitbvLogo.png" alt="Logo" className="logo-landing-page" />
          <h1 className="text-title-landing-page">FeedBack IESC</h1>
        </div>
        <Link className="button-landing-page" href="professors">
          <span className="top-key"></span>
          <span className="text">Explorează</span>
          <span className="bottom-key-1"></span>
          <span className="bottom-key-2"></span>
        </Link>
      </div>
      <div className="cube"></div>
      <div className="cube"></div>
      <div className="cube"></div>
      <div className="cube"></div>
      <div className="cube"></div>
      <div className="cube"></div>
    </div>
  )
}
