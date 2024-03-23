"use client";
import React ,{ useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./searchBar.module.css";
import TextField from "@mui/material/TextField";
export default function SearchBar() {
  const router = useRouter();
  const [text, setText] = useState("");

  useEffect(() => {
    if (!text) {
      router.push(`/professors`);
    } else {
      router.push(`/professors?search=${text}`);
    }
  }, [text, router]);

  return (
    <>
      <div className={styles.searchBar}>
        <div className="search">
          <TextField
            id="outlined-basic"
            variant="standard"
            fullWidth
            label="Caut&#259;"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
      </div>
    </>
  );
}
