"use client";
import React, { useState, useEffect, useRef } from "react";
import styles from "./dropdownArchive.module.css";
import Link from "next/link";
export default function DropdownArchive() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleDropdown = () => setIsOpen(!isOpen);

  return (
    <>
      <div ref={dropdownRef} className={styles.dropdown}>
        <button onClick={toggleDropdown} className={styles.dropbtn}>
          Arhivă ▼
        </button>
        {isOpen && (
          <div className={styles.dropdownContent}>
            <Link
              className={styles.buttonArchive}
              href={`/professors/archive/2023-2024`}
            >
              2023-2024
            </Link>
            <Link
              className={styles.buttonArchive}
              href={`/professors/archive/2023-2024`}
            >
              2024-2025
            </Link>
            <Link
              className={styles.buttonArchive}
              href={`/professors/archive/2023-2024`}
            >
              2025-2026
            </Link>
          </div>
        )}
      </div>
    </>
  );
}
