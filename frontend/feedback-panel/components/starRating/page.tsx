import styles from "./page.module.css";
import Image from "next/image";

interface StarRating {
  rating: number;
  ratingName: string;
  color: string;
}

export default function StarRating({ rating, ratingName, color }: StarRating) {
  let starSvgPath: string = "/svg/star.svg";
  if (color === "blue") starSvgPath = "/svg/star-blue.svg";
  else if (color === "red") starSvgPath = "/svg/star-red.svg";
  else if (color === "green") starSvgPath = "/svg/star-green.svg";

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
