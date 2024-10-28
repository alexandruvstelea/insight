import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { fetchProfessor } from "@/utils/fetchers/professors";
import {
  fetchProfessorAvgRating,
  fetchProfessorRatingsHistory,
} from "@/utils/fetchers/ratings";
import {
  SubjectWithAssociation,
  fetchSubjectsByProfessor,
} from "@/utils/fetchers/subjects";
import { NavigationBar } from "@/components/navigationBar/page";
import PolarAreaChart from "@/components/polarAreaChart/page";
import ChartsDropdown from "@/components/chartsDropdown/page";
import { EntityRating } from "@/components/entityRating/page";
import { reverseTransformName } from "@/utils/fetchers/professors";
import SubjectList from "@/components/subjectList/page";
import { NoData } from "@/components/noData/page";
import { ScrollButton } from "@/components/scrollButton/page";

interface ProfessorPageProps {
  params: {
    facultyAbbreviation: string;
    professorName: string;
  };
}

export default async function ProfessorPage({ params }: ProfessorPageProps) {
  const facultyAbbreviation: string = params.facultyAbbreviation;
  const transformedProfessorName: string = params.professorName;
  const professorName: { firstName: string; lastName: string } =
    reverseTransformName(transformedProfessorName);
  const faculty = await fetchFaculty(facultyAbbreviation);
  const professor = await fetchProfessor(
    professorName.firstName,
    professorName.lastName
  );
  const professorAverageRating = await fetchProfessorAvgRating(professor.id);
  const professorRatingsHistory = await fetchProfessorRatingsHistory(
    professor.id
  );
  const subjects: SubjectWithAssociation[] | false =
    await fetchSubjectsByProfessor(professor.id);

  const sortedSubjects = subjects
    ? subjects.sort((a, b) => {
        const nameA = a.name.toLowerCase();
        const nameB = b.name.toLowerCase();
        if (nameA < nameB) return -1;
        if (nameA > nameB) return 1;
        return 0;
      })
    : [];

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      {professor && professorAverageRating && sortedSubjects ? (
        <div className={styles.pageContainer}>
          <EntityRating
            entityName={`${professor.last_name} ${professor.first_name}`}
            rating={professorAverageRating.rating_overall_average}
          />
          <div className={styles.contentContainer}>
            <PolarAreaChart
              clarity={professorAverageRating.rating_clarity_average}
              relevance={professorAverageRating.rating_relevance_average}
              interactivity={
                professorAverageRating.rating_interactivity_average
              }
              comprehension={
                professorAverageRating.rating_comprehension_average
              }
              title="Medie Recenzii"
            />
            <ChartsDropdown subjectGraphData={professorRatingsHistory} />
            <SubjectList
              subjectsList={sortedSubjects}
              facultyAbbreviation={faculty.abbreviation}
              transformedProfessorName={transformedProfessorName}
            />
          </div>
        </div>
      ) : (
        <NoData />
      )}
    </>
  );
}
