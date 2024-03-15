"use client";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import TextField from "@mui/material/TextField";
import { Box, DialogContent, DialogActions } from "@mui/material";
import Button from "@mui/joy/Button";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";

export default function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem("access_token", data.access_token);
        router.push("/adminLogin/adminPage");
      } else if (response.status === 401) {
        toast.error("Credențiale greșite. Te rog încearcă din nou.");
      } else {
        toast.error("A apărut o eroare la autentificare.");
      }
    } catch (err) {
      toast.error("A apărut o eroare la conectarea la server.");
    }
  };

  return (
    <>
      <Header />
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable={false}
        pauseOnHover
        theme="colored"
      />
      <div className={styles.middleContainer}>
        <div className={styles.loginAdmin}>
          <div className={styles.adminTitle}>Admin Page</div>
          <Box>
            <form onSubmit={handleSubmit}>
              <DialogContent
                sx={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}
              >
                <TextField
                  type="text"
                  label="NAME"
                  name="username"
                  maxLength="20"
                  required
                  fullWidth
                  variant="standard"
                  autoComplete="on"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                  type="password"
                  label="PASSWORD"
                  name="password"
                  maxLength="20"
                  required
                  fullWidth
                  variant="standard"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </DialogContent>
              <DialogActions>
                <Button type="submit" sx={{ fontSize: "1.2rem" }}>
                  LOGIN
                </Button>
              </DialogActions>
            </form>
          </Box>
        </div>
      </div>
      <Footer />
    </>
  );
}
