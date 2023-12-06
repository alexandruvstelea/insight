import Link from "next/link";
import WavesSVG from "./WavesSVG";


export default function Header() {
  return (
    <>
      <div className="header">
        <div className="inner-header">
          <h1 className="header-title"><Link href="../professors">FeedBack IESC</Link></h1>
        </div>
        <WavesSVG />
      </div></>

  )
}