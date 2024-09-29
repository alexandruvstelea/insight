import styles from "./page.module.css";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import {
  fetchProfessor,
  fetchProfessorAvgRating,
} from "@/utils/fetchers/professors";
import { NavigationBar } from "@/components/navigationBar/page";
import Image from "next/image";
import StarRating from "@/components/starRating/page";
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
        <div className={styles.starRatings}>
          <StarRating
            rating={professorAverageRating.rating_overall_average}
            ratingName=""
            color="blue"
          />
          <StarRating
            rating={professorAverageRating.rating_interactivity_average}
            ratingName="Interactivitate"
            color="red"
          />
          <StarRating
            rating={professorAverageRating.rating_relevance_average}
            ratingName="Relevanta"
            color="green"
          />
        </div>
      </div>
    </>
  );
}
