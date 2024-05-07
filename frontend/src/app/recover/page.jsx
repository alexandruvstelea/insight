"use client";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import styles from "../login/page.module.css";
import Link from "next/link";
import React, { useState } from "react";
import { extractTextFromHTML } from "@/app/Actions/functions";
import { useRouter } from "next/navigation";

export default function UserRecover() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [showChangePassForm, setShowChangePassForm] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [code, setCode] = useState("");

  const handleRecover = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/request-reset`,
        {
          method: "POST",
          body: formData,
          credentials: "include",
        }
      );

      if (response.ok) {
        setError("");
        setShowChangePassForm(true);
      } else if (response.status === 400) {
        const errorMessage = await response.text();
        setError(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleChangePass = async (e) => {
    e.preventDefault();

    const formRecoverData = new FormData();
    formRecoverData.append("email", email);
    formRecoverData.append("new_password", newPassword);
    formRecoverData.append("code", code);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/reset`, {
        method: "POST",
        body: formRecoverData,
        credentials: "include",
      });

      if (response.ok) {
        setError("");
        router.push(`/login`);
      } else if (response.status === 400) {
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
          {!showChangePassForm ? (
            <div>
              <div className={styles.title}>Recover password</div>
              <form className={styles.form} onSubmit={handleRecover}>
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
                {error && <div className={styles.errorContainer}>{error}</div>}
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="submit"
                    value="Trimite cod"
                  />
                </div>
                <div className={styles.signupLink}>
                  Ai deja cont? <Link href="/login">Conectează-te!</Link>
                </div>
              </form>
            </div>
          ) : (
            <div>
              <div className={styles.title}>Change password</div>
              <form className={styles.form} onSubmit={handleChangePass}>
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
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className={styles.input}
                    type="password"
                    required
                  />
                  <label className={styles.label}>New password</label>
                </div>
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    required
                  />
                  <label className={styles.label}>Recover code</label>
                </div>
                {error && <div className={styles.errorContainer}>{error}</div>}
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="submit"
                    value="Schimbare parola"
                  />
                </div>
              </form>
            </div>
          )}
        </div>
        <Footer />
      </div>
    </>
  );
}
