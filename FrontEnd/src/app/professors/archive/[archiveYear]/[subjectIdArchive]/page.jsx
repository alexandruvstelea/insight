"use server";
import styles from "@/app/professors/[subjectId]/page.module.css";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import Chart from "@/components/subject/Chart";
import DegreeChart from "@/components/subject/DegreeChart";
import RatingOverview from "@/components/subject/RatingOverview";
import Comments from "@/components/subject/Comments";
import {
  fetchOldGraphData,
  fetchOldRatingsAverageData,
  fetchOldCommentsData,
  fetchOldDescriptionData,
} from "@/app/Actions/getOldSubjectData";

export default async function ArchiveInfoCourse({ params }) {
  const subjectId = params.subjectIdArchive;
  const year = params.archiveYear;
  const graphData = await fetchOldGraphData(subjectId, year);
  const ratingsAverage = await fetchOldRatingsAverageData(subjectId, year);
  const comments = await fetchOldCommentsData(subjectId, year);
  const description = await fetchOldDescriptionData(subjectId, year);

  const colors = [
    "rgba(0, 64, 193, 1)", //Total
    "rgba(5, 145, 248, 1)", //Clarity
    "rgba(39, 223, 243, 1)", //Comprehension
    "rgba(117, 220, 159, 1)", //Interactivity
    "rgba(0, 169, 165, 1)", //Relevance
  ];

  return (
    <>
      {graphData ? (
        <>
          <div className={styles.subjectsPageContainer}>
            <Header showArchive={true} />
            <div className={styles.content}>
              <div className={styles.titleContainer}>
                <h1 className={styles.professorName}>
                  {description.professor_name}
                </h1>
                <p className={styles.courseName}>
                  - {description.subject_name} -
                </p>
              </div>
              <div className={styles.mainContainer}>
                <div className={styles.dataContainer}>
                  <div className={styles.chartContainer}>
                    <Chart graphData={graphData} colors={colors} />
                  </div>
                  <div className={styles.rightContainer}>
                    <RatingOverview
                      ratingsAverage={ratingsAverage}
                      colors={colors}
                    />
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
      ) : (
        <>
          <div className={styles.subjectsPageContainer}>
            <Header showArchive={true} />
            <div className={styles.notFoundContainer}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                className={styles.infoSVG}
              >
                <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z" />
              </svg>
              NU EXIST&#258; DATE!
            </div>
            <Footer />
          </div>
        </>
      )}
    </>
  );
}
