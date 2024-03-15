import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import Chart from "@/components/infoCourse/Chart";
import RatingOverview from "@/components/infoCourse/RatingOverview";

import {
  fetchGraphData,
  fetchRatingsAverageData,
} from "@/app/Actions/getSubjectData";
import styles from "./page.module.css";

export default async function InfoCourse({ params }) {
  const graphData = await fetchGraphData(params.subjectId);
  const ratingsAverage = await fetchRatingsAverageData(params.subjectId);

  return (
    <>
      <Header />
      <div className={styles.containerCol}>
        <div className={styles.chartContainer}>
          <Chart graphData={graphData} />
        </div>
        <div className={styles.containerRow}>
          <RatingOverview ratingsAverage={ratingsAverage} />
        </div>
      </div>
      <Footer />
    </>
  );
}
