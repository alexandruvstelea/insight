import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import {
  fetchProfessor,
  fetchProfessorAvgRating,
} from "@/utils/fetchers/professors";
import { NavigationBar } from "@/components/navigationBar/page";
import Image from "next/image";

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
  const professorAverageRating: number = await fetchProfessorAvgRating(
    professorId
  );

  console.log(professorAverageRating);
  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      <div className={styles.pageContainer}>
        <h1 className={styles.professorName}>
          {professor.last_name} {professor.first_name}
        </h1>
        <Image
          width={80}
          height={80}
          src={`/svg/professors/${professor.last_name.toLowerCase()}.svg`}
          alt="Professor Avatar"
          className={styles.professorAvatar}
        />
        <h1>{professorAverageRating}</h1>
      </div>
    </>
  );
}
