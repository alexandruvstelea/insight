"use client";
import CustomSlider from "@/components/professors/CustomSlider";
import styles from "./page.module.css";
import TextField from "@mui/material/TextField";
import { useState } from "react";
import DropdownArchive from "@/components/infoCourse/DropdownArchive";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";

export default function Professors() {
  const [searchTerm, setSearchTerm] = useState("");
  const [isError404, setIsError404] = useState(false);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleError = (error) => {
    if (error) {
      setIsError404(true);
    }
  };

  return (
    <>
      {isError404 ? (
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
              NU EXISTĂ DATE!
            </div>
            <Footer />
          </div>
        </>
      ) : (
        <div className={styles.professorsPageContainer}>
          <Header />
          <div className={styles.searchBar}>
            <div className="search">
              <TextField
                id="outlined-basic"
                variant="standard"
                fullWidth
                label="Caută"
                value={searchTerm}
                onChange={handleSearchChange}
              />
            </div>
            <div className={styles.secondaryDropdown}>
              <DropdownArchive />
            </div>
          </div>
          <CustomSlider onError={handleError} searchTerm={searchTerm} />
          <Footer />
        </div>
      )}
    </>
  );
}
