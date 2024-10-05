import styles from "./page.module.css";
import Image from "next/image";

interface StarRating {
  rating: number;
  ratingName: string;
}

export default function StarRating({ rating, ratingName }: StarRating) {
  let starSvgPath: string = "/svg/star-blue.svg";

  return (
    <>
      <div className={styles.starRating}>
        <h1>{ratingName}</h1>
        <div className={styles.rating}>
          <Image
            width={40}
            height={40}
            src={starSvgPath}
            alt="Star SVG"
            className={styles.starImage}
          />
          <h2>{rating}</h2>
        </div>
      </div>
    </>
  );
}
