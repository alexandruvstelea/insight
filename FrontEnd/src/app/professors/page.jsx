'use client'
import CustomSlider from "@/components/professors/CustomSlider";
import styles from './page.module.css';
import TextField from "@mui/material/TextField";
import { useState } from 'react'


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


      {
        isError404 ? (
          <div className={styles.cont} >
            <div className={styles.noFoundContainer}>NU EXISTĂ DATE!</div>
          </div>
        ) : (

          <div className={styles.rowContainer}>
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
            </div>
            <CustomSlider onError={handleError} searchTerm={searchTerm} />
          </div >
        )
      }
    </>
  )
}
