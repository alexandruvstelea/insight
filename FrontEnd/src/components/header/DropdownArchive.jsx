import React, { useState, useEffect, useRef } from "react";
import styles from "./dropdownArchive.module.css";

export default function DropdownArchive() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState("Arhiv&#259;");
  const dropdownRef = useRef(null);

  useEffect(() => {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1;
    const adjustedYear = currentMonth < 10 ? currentYear - 1 : currentYear;

    const storedYear = sessionStorage.getItem("rangeYear") || "Arhiv&#259;";

    if (
      !sessionStorage.getItem("selectedYear") ||
      sessionStorage.getItem("selectedYear") === ""
    ) {
      sessionStorage.setItem("selectedYear", adjustedYear);
    }

    setSelectedYear(storedYear);

    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleDropdown = () => setIsOpen(!isOpen);

  const handleSelectYear = (rangeYear) => {
    const selectedYear = rangeYear.split("-")[0];
    setSelectedYear(rangeYear);
    sessionStorage.setItem("selectedYear", selectedYear);
    sessionStorage.setItem("rangeYear", rangeYear);
    setIsOpen(false);
    window.location.reload();
  };

  return (
    <>
      <div ref={dropdownRef} className={styles.dropdown}>
        <button onClick={toggleDropdown} className={styles.dropbtn}>
          {selectedYear}
        </button>
        {isOpen && (
          <div className={styles.dropdownContent}>
            <button onClick={() => handleSelectYear("2023-2024")}>
              2023-2024
            </button>
            <button onClick={() => handleSelectYear("2024-2025")}>
              2024-2025
            </button>
            <button onClick={() => handleSelectYear("2025-2026")}>
              2025-2026
            </button>
          </div>
        )}
      </div>
    </>
  );
}
