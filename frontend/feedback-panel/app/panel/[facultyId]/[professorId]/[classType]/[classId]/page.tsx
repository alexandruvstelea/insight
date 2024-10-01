import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { fetchProfessor } from "@/utils/fetchers/professors";
import { NavigationBar } from "@/components/navigationBar/page";

interface ClassPageProps {
  params: {
    facultyId: number;
    professorId: number;
    classType: string;
    classId: number;
  };
}

export default async function ClassPage({ params }: ClassPageProps) {
  const facultyId: number = params.facultyId;
  const professorId: number = params.professorId;
  const professor = await fetchProfessor(professorId);
  const faculty = await fetchFaculty(facultyId);

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
    </>
  );
}
