"use server";
import styles from "./page.module.css";
import { fetchProfessorsData } from "../Actions/getProfessorData";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import CustomSlider from "@/components/professors/customSlider/CustomSlider";
import SearchBar from "@/components/professors/searchBar/SearchBar";

export default async function Professors({ searchParams }) {
  const search = searchParams.search;

  const professors = await fetchProfessorsData();

  const filteredProfessors = search
    ? [
        ...professors.filter(
          (professor) =>
            professor.first_name.toLowerCase().includes(search.toLowerCase()) ||
            professor.last_name.toLowerCase().includes(search.toLowerCase())
        ),
        ...professors.filter(
          (professor) =>
            !professor.first_name
              .toLowerCase()
              .includes(search.toLowerCase()) &&
            !professor.last_name.toLowerCase().includes(search.toLowerCase())
        ),
      ]
    : professors;

  return (
    <>
      {professors && professors.length > 0 ? (
        <>
          <div className={styles.professorsPageContainer}>
            <Header showArchive={true} />
            <div className={styles.contentContainer}>
              <SearchBar />
              <CustomSlider professors={filteredProfessors} />
            </div>

            <Footer />
          </div>
        </>
      ) : (
        <>
          <div className={styles.professorsPageContainer}>
            <Header showArchive={true} />
            <div className={styles.notFoundContainer}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                className={styles.infoSVG}
              >
                <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z" />
              </svg>
              NU EXIST&#258; DATE!
            </div>
            <Footer />
          </div>
        </>
      )}
    </>
  );
}
