import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { fetchProfessor } from "@/utils/fetchers/professors";
import { NavigationBar } from "@/components/navigationBar/page";
import {
  fetchSubjectAverage,
  fetchSubjectGraphData,
} from "@/utils/fetchers/subjects";
import PolarAreaChart from "@/components/polarAreaChart/page";
import BarChart from "@/components/barChart/page";

interface ClassPageProps {
  params: {
    facultyId: number;
    professorId: number;
    subjectType: string;
    subjectId: number;
  };
}

export default async function ClassPage({ params }: ClassPageProps) {
  const facultyId: number = params.facultyId;
  const professorId: number = params.professorId;
  const subjectType: string = params.subjectType;
  const subjectId: number = params.subjectId;
  const professor = await fetchProfessor(professorId);
  const faculty = await fetchFaculty(facultyId);
  const subjectAverage = await fetchSubjectAverage(
    professorId,
    subjectId,
    subjectType
  );

  const subjectGraphData = await fetchSubjectGraphData(
    professorId,
    subjectId,
    subjectType
  );

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      <div className={styles.pageContainer}>
        <BarChart
          ratings_data={subjectGraphData}
          rating_type="overall"
          label="Medie Recenzii"
        />
        <BarChart
          ratings_data={subjectGraphData}
          rating_type="interactivity"
          label="Recenzii Interactivitate"
        />
        <BarChart
          ratings_data={subjectGraphData}
          rating_type="relevance"
          label="Recenzii Relevanta"
        />
        <BarChart
          ratings_data={subjectGraphData}
          rating_type="comprehension"
          label="Recenzii Intelegere"
        />
        <BarChart
          ratings_data={subjectGraphData}
          rating_type="clarity"
          label="Recenzii Claritate"
        />
        {/* <PolarAreaChart
          clarity={subjectAverage.rating_clarity_average}
          relevance={subjectAverage.rating_relevance_average}
          interactivity={subjectAverage.rating_interactivity_average}
          comprehension={subjectAverage.rating_comprehension_average}
          title=""
        /> */}
      </div>
    </>
  );
}
