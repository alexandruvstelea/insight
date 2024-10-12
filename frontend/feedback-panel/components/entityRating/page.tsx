import styles from "./page.module.css";
import StarRating from "../starRating/page";

interface EntityRating {
  entityName: string;
  entityType?: string;
  rating?: number;
}

export function EntityRating({ entityName, entityType, rating }: EntityRating) {
  return (
    <>
      <div className={styles.container}>
        <h1 className={styles.entity}>{entityName}</h1>
        {entityType && <h2 className={styles.entityType}>{entityType}</h2>}
        {rating && <StarRating rating={rating} size="default" />}
      </div>
    </>
  );
}
