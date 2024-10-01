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
import ClassButton from "@/components/classButton/page";

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
  const subjects: ProfessorSubjects | false | undefined =
    await fetchSubjectsByProfessor(professorId);

  const renderClasses = (courses: any, title: string, type: string) => {
    return (
      courses?.length > 0 && (
        <>
          <h1>{title}</h1>
          {courses.map((course: any) => (
            <ClassButton
              key={course.id}
              classId={course.id}
              className={course.name}
              classType={type}
              facultyId={facultyId}
              professorId={professorId}
            />
          ))}
        </>
      )
    );
  };

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
          {subjects && renderClasses(subjects.courses, "Cursuri", "course")}
          {subjects &&
            renderClasses(subjects.laboratories, "Laboratoare", "laboratory")}
          {subjects && renderClasses(subjects.seminars, "Seminare", "seminar")}
          {subjects && renderClasses(subjects.projects, "Proiecte", "project")}
        </div>
      </div>
    </>
  );
}
