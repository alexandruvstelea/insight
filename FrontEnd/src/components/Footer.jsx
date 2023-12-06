import Image from 'next/image'
import Link from "next/link";
export default function Footer() {
  return (
    <>
      <div className="copy-right">
        <div className="copy-right-content">
          <i className="fa-solid fa-copyright"></i>
          © Developed by
          <a href="https://www.linkedin.com/in/cristianandreisava" target="_blank" rel="noopener noreferrer">Sava Andrei</a>
          and
          <a href="https://www.linkedin.com/in/alexandrustelea" target="_blank" rel="noopener noreferrer">Stelea Alexandru</a>
        </div>
        <div className="copy-right-admin-logo">
          <Link href="adminLogin"><Image width={27} height={27} src="/images/adminLogo.png" alt="ADMIN" /></Link>
        </div>
      </div>
    </>
  )
}