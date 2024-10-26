"use server";
import { NavigationBar } from "@/components/navigationBar/page";
import { fetchFaculty } from "@/utils/fetchers/faculties";
import ProfessorCard from "@/components/professorCard/page";
import FacultyStatistics from "@/components/facultyStatistics/page";
import SearchBar from "@/components/searchBar/page";
import styles from "./page.module.css";
import {
  fetchProfessorsCount,
  fetchRoomsCount,
  fetchRatingsCount,
} from "@/utils/fetchers/counters";
import { NoData } from "@/components/noData/page";

interface PanelPageProps {
  params: {
    facultyAbbreviation: string;
  };
  searchParams: {
    search?: string;
  };
}

export default async function PanelPage({
  params,
  searchParams,
}: PanelPageProps) {
  const facultyAbbreviation: string = params.facultyAbbreviation;
  const searchText: string = searchParams.search || "";
  const faculty = await fetchFaculty(facultyAbbreviation);
  const professorsCount: number = await fetchProfessorsCount(faculty.id);
  const roomsCount: number = await fetchRoomsCount(faculty.id);
  const ratingsCount: number = await fetchRatingsCount(faculty.id);
  const professors = faculty.professors;

  const removeDiacritics = (str: string): string => {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  };

  const filteredProfessors: any[] = searchText
    ? professors
        .filter((professor: any) => {
          const normalizedFirstName = removeDiacritics(
            professor.first_name.toLowerCase()
          );
          const normalizedLastName = removeDiacritics(
            professor.last_name.toLowerCase()
          );
          const normalizedSearchText = removeDiacritics(
            searchText.toLowerCase()
          );

          return (
            normalizedFirstName.includes(normalizedSearchText) ||
            normalizedLastName.includes(normalizedSearchText)
          );
        })
        .sort((a: any, b: any) => {
          const lastNameA = a.last_name.toLowerCase();
          const lastNameB = b.last_name.toLowerCase();

          if (lastNameA < lastNameB) return -1;
          if (lastNameA > lastNameB) return 1;
          return 0;
        })
    : professors.sort((a: any, b: any) => {
        const lastNameA = a.last_name.toLowerCase();
        const lastNameB = b.last_name.toLowerCase();

        if (lastNameA < lastNameB) return -1;
        if (lastNameA > lastNameB) return 1;
        return 0;
      });

  return (
    <>
      <NavigationBar facultyAbbreviation={faculty.abbreviation} />
      {professorsCount && roomsCount && ratingsCount && filteredProfessors ? (
        <div className={styles.pageContainer}>
          <div className={styles.statistics}>
            <FacultyStatistics statistic={professorsCount} name="Profesori" />
            <FacultyStatistics statistic={roomsCount} name="Săli" />
            <FacultyStatistics statistic={ratingsCount} name="Recenzii" />
          </div>
          <div className={styles.professorsList}>
            <SearchBar facultyAbbreviation={facultyAbbreviation} />
            {filteredProfessors && filteredProfessors.length > 0 ? (
              <>
                {filteredProfessors.map((professor: any) => (
                  <ProfessorCard
                    key={professor.id}
                    professorID={professor.id}
                    firstName={professor.first_name}
                    lastName={professor.last_name}
                    gender={professor.gender}
                    facultyAbbreviation={facultyAbbreviation}
                  />
                ))}
              </>
            ) : (
              <h1 className={styles.notFound}>Nu s-au găsit profesori.</h1>
            )}
          </div>
        </div>
      ) : (
        <NoData />
      )}
    </>
  );
}
