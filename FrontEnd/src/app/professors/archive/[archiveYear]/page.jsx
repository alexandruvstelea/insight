"use server";
import styles from "@/app/professors/page.module.css";
import { fetchOldProfessorsData } from "@/app/Actions/getOldProfessorData";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import CustomSlider from "@/components/professors/CustomSlider";
import SearchBar from "@/components/professors/SearchBar";
export default async function Professors({ searchParams, params }) {
  const search = searchParams.search;
  console.log(search);
  const professors = await fetchOldProfessorsData(params.archiveYear);

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
            <Header />
            <SearchBar />
            <CustomSlider professors={filteredProfessors} />
            <Footer />
          </div>
        </>
      ) : (
        <>
          <div className={styles.professorsPageContainer}>
            <Header />

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
