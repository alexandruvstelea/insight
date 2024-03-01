import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import Chart from "@/components/infoCourse/Chart";
import { fetchGraphData } from "@/app/Actions/getSubjectsData";
import styles from "./page.module.css";

export default async function InfoCourse({ params }) {
  const graphData = await fetchGraphData(params.subjectId);
  return (
    <>
      <Header />
      <div className={styles.containerCol}>
        <div className={styles.chartContainer}>
          <Chart graphData={graphData} />
        </div>
        {/* <div className={styles.containerRow}>
          <RatingOverview subjectId={subjectId} onError={handleError} />
          <Likes likesData={likesData} />
        </div> */}
      </div>

      <h1>Informatii despre Curs {params.subjectId}</h1>
      <Footer />
    </>
  );
}
