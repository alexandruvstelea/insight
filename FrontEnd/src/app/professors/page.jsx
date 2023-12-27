'use client'
import CustomSlider from "@/components/professors/CustomSlider";
import styles from './page.module.css';
import TextField from "@mui/material/TextField";
import { useState } from 'react'
import DropdownArchive from "@/components/infoCourse/DropdownArchive";

export default function Professors() {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };



  return (
    <>
      <DropdownArchive />
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
        <CustomSlider searchTerm={searchTerm} />

      </div >
    </>
  )
}
