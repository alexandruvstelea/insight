import styles from "./page.module.css";
import Image from "next/image";

interface StarRatingProps {
  rating: number;
  ratingName: string;
  size?: "small" | "default";
}

export default function StarRating({
  rating,
  ratingName,
  size = "default",
}: StarRatingProps) {
  const starSvgPath: string = "/svg/star-blue.svg";

  const ratingClass =
    size === "small" ? styles.smallRating : styles.defaultRating;

  return (
    <div className={`${styles.starRating} ${ratingClass}`}>
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
  );
}
