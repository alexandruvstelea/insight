"use client";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import styles from "./page.module.css";
import Link from "next/link";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { extractTextFromHTML } from "@/app/Actions/functions";
import { fetchCheckLogin, fetchLogoutUser } from "@/app/Actions/getUserData";
export default function UserLogin() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        setError("");
        const loggedIn = await fetchCheckLogin();
        if (loggedIn.type === 0) {
          router.push("/loginAdmin/admin");
        } else if (loggedIn.type === 1) {
          fetchLogoutUser();
          router.push("/professors");
        }
      } else if (response.status === 401 || response.status === 400) {
        const errorMessage = await response.text();
        setError(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <div className={styles.mainContiner}>
        <Header showArchive={false} />
        <div className={styles.wrapper}>
          <div className={styles.title}>Login Admin</div>
          <form className={styles.form} onSubmit={handleSubmit}>
            <div className={styles.field}>
              <input
                className={styles.input}
                type="text"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <label className={styles.label}>Email Address</label>
            </div>
            <div className={styles.field}>
              <input
                className={styles.input}
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <label className={styles.label}>Password</label>
            </div>
            {error && <div className={styles.errorContainer}>{error}</div>}
            <div className={styles.content}>
              <div className={styles.passLink}>
                <Link href="/recover">Recuperare parolă!</Link>
              </div>
            </div>
            <div className={styles.field}>
              <input className={styles.input} type="submit" value="Login" />
            </div>
          </form>
        </div>
        <Footer />
      </div>
    </>
  );
}
