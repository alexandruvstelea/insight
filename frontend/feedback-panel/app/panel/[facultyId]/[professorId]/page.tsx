import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import {
  fetchProfessor,
  fetchProfessorAvgRating,
} from "@/utils/fetchers/professors";
import {
  ProfessorSubjects,
  fetchSubjectsByProfessor,
} from "@/utils/fetchers/subjects";
import { NavigationBar } from "@/components/navigationBar/page";
import PolarAreaChart from "@/components/polarAreaChart/page";
import Link from "next/link";

interface ProfessorPageProps {
  params: {
    facultyId: number;
    professorId: number;
  };
}

export default async function ProfessorPage({ params }: ProfessorPageProps) {
  const facultyId: number = params.facultyId;
  const professorId: number = params.professorId;
  const faculty = await fetchFaculty(facultyId);
  const professor = await fetchProfessor(professorId);
  const professorAverageRating = await fetchProfessorAvgRating(professorId);
  const subjects: ProfessorSubjects | false = await fetchSubjectsByProfessor(
    professorId
  );
  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      <div className={styles.pageContainer}>
        <h1 className={styles.professorName}>
          {professor.last_name} {professor.first_name}
        </h1>
        <PolarAreaChart
          clarity={professorAverageRating.rating_clarity_average}
          relevance={professorAverageRating.rating_relevance_average}
          interactivity={professorAverageRating.rating_interactivity_average}
          comprehension={professorAverageRating.rating_comprehension_average}
          average={professorAverageRating.rating_overall_average}
        />
        <div className={styles.professorClasses}>
          <h1>Cursuri</h1>

          {subjects &&
            subjects.courses.map((course: any, index: number) => (
              <Link
                key={index}
                href={{
                  pathname: `/panel`,
                }}
                className={styles.courseButton}
              >
                {course}
              </Link>
            ))}
        </div>
      </div>
    </>
  );
}
