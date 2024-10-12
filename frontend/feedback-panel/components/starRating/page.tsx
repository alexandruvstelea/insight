import styles from "./page.module.css";
import Image from "next/image";

interface StarRatingProps {
  rating: number;
  size?: "small" | "default";
}

export default function StarRating({
  rating,
  size = "default",
}: StarRatingProps) {
  const starFullSvgPath: string = "/svg/star-blue.svg";
  const starHalfSvgPath: string = "/svg/star-half-blue.svg";
  const starEmptySvgPath: string = "/svg/star-empty-blue.svg";

  const ratingClass =
    size === "small" ? styles.smallRating : styles.defaultRating;

  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.1 && rating % 1 <= 1;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

  return (
    <div className={`${styles.starRating} ${ratingClass}`}>
      <div className={styles.rating}>
        {Array(fullStars)
          .fill(0)
          .map((_, index) => (
            <Image
              key={`full-star-${index}`}
              width={40}
              height={40}
              src={starFullSvgPath}
              alt="Full Star"
              className={styles.starImage}
            />
          ))}

        {hasHalfStar && (
          <Image
            width={40}
            height={40}
            src={starHalfSvgPath}
            alt="Half Star"
            className={styles.starImage}
          />
        )}

        {Array(emptyStars)
          .fill(0)
          .map((_, index) => (
            <Image
              key={`empty-star-${index}`}
              width={40}
              height={40}
              src={starEmptySvgPath}
              alt="Empty Star"
              className={styles.starImage}
            />
          ))}

        <h2>{rating}</h2>
      </div>
    </div>
  );
}
