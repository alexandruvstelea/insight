"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";

interface SearchBar {
  facultyAbbreviation: string;
}

export default function SearchBar({ facultyAbbreviation }: SearchBar) {
  const router = useRouter();
  const [text, setText] = useState("");

  useEffect(() => {
    if (!text) {
      router.push(`/panel/${facultyAbbreviation}`);
    } else {
      router.push(`/panel/${facultyAbbreviation}?search=${text}`);
    }
  }, [text, router]);

  return (
    <>
      <div className={styles.searchBar}>
        <input
          type="text"
          placeholder="Caut&#259; profesor"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className={styles.searchInput}
        />
      </div>
    </>
  );
}
