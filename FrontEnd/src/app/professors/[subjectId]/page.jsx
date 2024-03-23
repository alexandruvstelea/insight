import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import Chart from "@/components/subject/Chart";
import DegreeChart from "@/components/subject/DegreeChart";
import RatingOverview from "@/components/subject/RatingOverview";
import Comments from "@/components/subject/Comments";
import styles from "./page.module.css";
import {
  fetchGraphData,
  fetchRatingsAverageData,
  fetchCommentsData,
} from "@/app/Actions/getSubjectData";

export default async function InfoCourse({ params }) {
  const subjectId = params.subjectId;
  const graphData = await fetchGraphData(subjectId);
  const ratingsAverage = await fetchRatingsAverageData(subjectId);
  const comments = await fetchCommentsData(subjectId);
  return (
    <>
      <div className="globalContainer">
        <Header />
        <div className="content">
          <div className={styles.titleContainer}>
            <h1 className={styles.professorName}>Numele la prof</h1>
            <p className={styles.courseName}>- cursul - </p>
          </div>
          <div className={styles.mainContainer}>
            <div className={styles.dataContainer}>
              <div className={styles.chartContainer}>
                <Chart graphData={graphData} />
              </div>
              <div className={styles.rightContainer}>
                <RatingOverview ratingsAverage={ratingsAverage} />
                <div className={styles.pieChart}>
                  <DegreeChart />
                </div>
              </div>
            </div>
            <Comments subjectId={subjectId} comments={comments} />
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}
