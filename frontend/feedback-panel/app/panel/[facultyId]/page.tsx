"use server";
import { NavigationBar } from "@/components/navigationBar/page";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import ProfessorCard from "@/components/professorCard/page";
import FacultyStatistics from "@/components/facultyStatistics/page";
import SearchBar from "@/components/searchBar/page";
import styles from "./page.module.css";

interface PanelPageProps {
  params: {
    facultyId: number;
  };
  searchParams: {
    search?: string;
  };
}

export default async function PanelPage({
  params,
  searchParams,
}: PanelPageProps) {
  const facultyId: number = params.facultyId;
  const searchText: string = searchParams.search || "";
  const faculty = await fetchFaculty(facultyId);
  const professors = faculty.professors;
  const filteredProfessors = searchText
    ? [
        ...professors.filter(
          (professor: any) =>
            professor.first_name
              .toLowerCase()
              .includes(searchText.toLowerCase()) ||
            professor.last_name.toLowerCase().includes(searchText.toLowerCase())
        ),
      ]
    : professors;

  console.log(searchText);

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      <div className={styles.pageContainer}>
        <div className={styles.statistics}>
          <FacultyStatistics statistic={6} name="Profesori" />
          <FacultyStatistics statistic={2} name="Săli" />
          <FacultyStatistics statistic={3760} name="Recenzii" />
        </div>
        <div className={styles.professorsList}>
          <SearchBar facultyId={Number(facultyId)} />
          {filteredProfessors && filteredProfessors.length > 0 ? (
            <>
              {filteredProfessors.map((professor: any) => (
                <ProfessorCard
                  key={professor.id}
                  professorID={professor.id}
                  firstName={professor.first_name}
                  lastName={professor.last_name}
                  gender={professor.gender}
                  facultyId={facultyId}
                />
              ))}
              {filteredProfessors.map((professor: any) => (
                <ProfessorCard
                  key={professor.id}
                  professorID={professor.id}
                  firstName={professor.first_name}
                  lastName={professor.last_name}
                  gender={professor.gender}
                  facultyId={facultyId}
                />
              ))}
            </>
          ) : (
            <p>Nu s-au gasit profesori.</p>
          )}
        </div>
      </div>
    </>
  );
}
