import { NavigationBar } from "@/components/navigationBar/page";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { fetchProfessorAvgRating } from "@/utils/fetchers/professors";
import ProfessorsSlider from "@/components/professorsSlider/page";
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

  const professorsWithRatings = await Promise.all(
    professors.map(async (professor: any) => {
      const response = await fetchProfessorAvgRating(professor.id);
      return {
        ...professor,
        avgRating: response.average,
      };
    })
  );

  return (
    <>
      <NavigationBar />
      <div className={styles.pageContainer}>
        <h1 className={styles.facultyName}>{faculty.abbreviation}</h1>
        <div className={styles.professorsList}>
          <ProfessorsSlider professors={professorsWithRatings} />
        </div>
      </div>
    </>
  );
}
