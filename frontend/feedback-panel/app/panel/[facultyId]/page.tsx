import { NavigationBar } from "@/components/navigationBar/page";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import ProfessorCard from "@/components/professorCard/page";
import FacultyStatistics from "@/components/facultyStatistics/page";
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
      <div className={styles.pageContainer}>
        <div className={styles.statistics}>
          <h1 className={styles.facultyName}>{faculty.name}</h1>
          <FacultyStatistics statistic={6} name="Profesori" />
          <FacultyStatistics statistic={2} name="Săli" />
          <FacultyStatistics statistic={3760} name="Recenzii" />
        </div>
        <div className={styles.professorsList}>
          <h1 className={styles.listName}>Listă profesori</h1>
          {professors && professors.length > 0 ? (
            <>
              {professors.map((professor: any) => (
                <ProfessorCard
                  key={professor.id}
                  professorID={professor.id}
                  firstName={professor.first_name}
                  lastName={professor.last_name}
                  gender={professor.gender}
                />
              ))}
              {professors.map((professor: any) => (
                <ProfessorCard
                  key={professor.id}
                  professorID={professor.id}
                  firstName={professor.first_name}
                  lastName={professor.last_name}
                  gender={professor.gender}
                />
              ))}
              {professors.map((professor: any) => (
                <ProfessorCard
                  key={professor.id}
                  professorID={professor.id}
                  firstName={professor.first_name}
                  lastName={professor.last_name}
                  gender={professor.gender}
                />
              ))}
            </>
          ) : (
            <p>No professors available.</p>
          )}
        </div>
      </div>
    </>
  );
}
