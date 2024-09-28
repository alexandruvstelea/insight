import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import { NavigationBar } from "@/components/navigationBar/page";

interface ProfessorPageProps {
  params: {
    facultyId: number;
  };
}

export default async function ProfessorPage({ params }: ProfessorPageProps) {
  const facultyId: number = params.facultyId;
  const faculty = await fetchFaculty(facultyId);
  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
    </>
  );
}
