"use client";
import styles from "./searchBar.module.css";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useDebounce } from "use-debounce";
import TextField from "@mui/material/TextField";
export default function SearchBar() {
  const router = useRouter();
  const [text, setText] = useState("");
  const [query] = useDebounce(text, 500);

  useEffect(() => {
    if (!query) {
      router.push(`/professors`);
    } else {
      router.push(`/professors?search=${query}`);
    }
  }, [query, router]);

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
