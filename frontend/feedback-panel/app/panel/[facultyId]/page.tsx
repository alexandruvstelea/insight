import { NavigationBar } from "@/components/navigationBar/page";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import ProfessorCard from "@/components/professorCard/page";
import styles from "./page.module.css";

interface PanelPageProps {
  params: {
    facultyId: string;
  };
}

export default async function PanelPage({ params }: PanelPageProps) {
  const { facultyId } = params;
  const faculty = await fetchFaculty(Number(facultyId));
  const professors = faculty.professors;
  return (
    <>
      <NavigationBar />
      <h1 className={styles.facultyName}>{faculty.abbreviation}</h1>
      <div className={styles.professorsList}>
        {professors.map((professor: any) => (
          <ProfessorCard
            key={professor.id}
            professorID={professor.id}
            firstName={professor.first_name}
            lastName={professor.last_name}
            gender={professor.gender}
          />
        ))}
      </div>
    </>
  );
}
