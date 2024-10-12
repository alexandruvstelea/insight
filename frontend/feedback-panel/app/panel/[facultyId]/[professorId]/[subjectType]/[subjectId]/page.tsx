import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { fetchProfessor } from "@/utils/fetchers/professors";
import { NavigationBar } from "@/components/navigationBar/page";
import {
  fetchSubject,
  fetchSubjectAverage,
  fetchSubjectGraphData,
} from "@/utils/fetchers/subjects";
import PolarAreaChart from "@/components/polarAreaChart/page";
import ChartsDropdown from "@/components/chartsDropdown/page";
import StarRating from "@/components/starRating/page";
import { EntityRating } from "@/components/entityRating/page";

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
  const subject = await fetchSubject(subjectId);
  const professor = await fetchProfessor(professorId);
  const faculty = await fetchFaculty(facultyId);
  const subjectAverage = await fetchSubjectAverage(
    professorId,
    subjectId,
    subjectType
  );
  const subjectGraphData = await fetchSubjectGraphData(
    professorId,
    subject.id,
    subjectType
  );

  const getSubjectType = (subjectType: string): string => {
    switch (subjectType) {
      case "course":
        return "Curs";
      case "laboratory":
        return "Laborator";
      case "seminar":
        return "Seminar";
      case "project":
        return "Proiect";
      default:
        return "";
    }
  };

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      <div className={styles.pageContainer}>
        <EntityRating
          entityName={`${subject.name}`}
          entityType={getSubjectType(subjectType)}
          rating={subjectAverage.rating_overall_average}
        />
        <div className={styles.chartsContainer}>
          <ChartsDropdown subjectGraphData={subjectGraphData} />
          <PolarAreaChart
            clarity={subjectAverage.rating_clarity_average}
            relevance={subjectAverage.rating_relevance_average}
            interactivity={subjectAverage.rating_interactivity_average}
            comprehension={subjectAverage.rating_comprehension_average}
            title="Medie pe Categorii"
          />
        </div>
      </div>
    </>
  );
}
