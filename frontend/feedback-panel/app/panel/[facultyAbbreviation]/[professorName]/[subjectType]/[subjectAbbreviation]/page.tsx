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
import { EntityRating } from "@/components/entityRating/page";
import { reverseTransformName } from "@/utils/fetchers/professors";

interface ClassPageProps {
  params: {
    facultyAbbreviation: string;
    professorName: string;
    subjectType: string;
    subjectAbbreviation: string;
  };
}

export default async function ClassPage({ params }: ClassPageProps) {
  const facultyAbbreviation: string = params.facultyAbbreviation;
  const transformedProfessorName: string = params.professorName;
  const professorName: { firstName: string; lastName: string } =
    reverseTransformName(transformedProfessorName);
  const subjectType: string = params.subjectType;
  const subjectAbbreviation: string = params.subjectAbbreviation;
  const subject = await fetchSubject(subjectAbbreviation);
  const professor = await fetchProfessor(
    professorName.firstName,
    professorName.lastName
  );
  const faculty = await fetchFaculty(facultyAbbreviation);
  const subjectAverage = await fetchSubjectAverage(
    professor.id,
    subject.id,
    subjectType
  );
  const subjectGraphData = await fetchSubjectGraphData(
    professor.id,
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
