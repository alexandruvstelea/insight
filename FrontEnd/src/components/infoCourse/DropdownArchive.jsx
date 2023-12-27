import React, { useState, useEffect } from "react";
import styles from './dropdownArchive.module.css'

export default function DropdownArchive() {

  const [isOpen, setIsOpen] = useState(false);

  const [selectedYear, setSelectedYear] = useState('Arhiva');


  useEffect(() => {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;

    const storedYear = sessionStorage.getItem('rangeYear') || adjustedYear;

    if (!sessionStorage.getItem('selectedYear') || sessionStorage.getItem('selectedYear') === '') {
      sessionStorage.setItem('selectedYear', adjustedYear);
    }

    setSelectedYear(storedYear);
  }, []);


  const toggleDropdown = () => setIsOpen(!isOpen);

  const handleSelectYear = (rangeYear) => {
    const selectedYear = rangeYear.split('-')[0];
    setSelectedYear(rangeYear);
    sessionStorage.setItem('selectedYear', selectedYear);
    sessionStorage.setItem('rangeYear', rangeYear);
    setIsOpen(false);
    window.location.reload();
  };

  return (
    <>
      <div className={styles.dropdown}>
        <button onClick={toggleDropdown} className={styles.dropbtn}> {selectedYear}</button>
        {isOpen && (
          <div className={styles.dropdownContent}>
            <a onClick={() => handleSelectYear('2023-2024')} href="#">2023-2024</a>
            <a onClick={() => handleSelectYear('2024-2025')} href="#">2024-2025</a>
            <a onClick={() => handleSelectYear('2025-2026')} href="#">2025-2026</a>
          </div>
        )}
      </div>
    </>
  )
}