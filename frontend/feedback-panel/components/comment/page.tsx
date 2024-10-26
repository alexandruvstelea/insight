import styles from "./page.module.css";

interface Comment {
  text: string;
  timestamp: string;
}

export default function Comment({ text, timestamp }: Comment) {
  const author: string = "Student Anonim";
  const date = timestamp.split("T")[0];
  return (
    <>
      <div className={styles.commentContainer}>
        <h1>{author}</h1>
        <h2>{date}</h2>
        <p>{text}</p>
      </div>
    </>
  );
}
