"use client";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";
import styles from "../userLogin/page.module.css";
import Link from "next/link";
import { fetchProgrammesData } from "@/app/Actions/getSubjectData";
import { extractTextFromHTML } from "@/app/Actions/functions";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function UserRegister() {
  const router = useRouter();
  const [programmes, setProgrammes] = useState([]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [programmeId, setProgrammeId] = useState();
  const [error, setError] = useState("");

  const [code, setCode] = useState("");
  const [showActivationForm, setShowActivationForm] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    const registrationFormData = new FormData();
    registrationFormData.append("email", email);
    registrationFormData.append("password", password);
    registrationFormData.append("programme_id", programmeId);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/register`,
        {
          method: "POST",
          body: registrationFormData,
          credentials: 'include',
        }
      );

      if (response.ok) {
        setError("");
        setShowActivationForm(true);
      } else if (response.status === 400) {
        const errorMessage = await response.text();
        setError(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleActivation = async (e) => {
    e.preventDefault();

    const activationFormData = new FormData();
    activationFormData.append("email", email);
    activationFormData.append("password", password);
    activationFormData.append("code", code);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/activate`,
        {
          method: "POST",
          body: activationFormData,
          credentials: 'include',
        }
      );

      if (response.ok) {
        setError("");
        router.push(`/userLogin`);
      } else if (response.status === 400) {
        const errorMessage = await response.text();
        setError(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleResendCode = async (e) => {
    e.preventDefault();

    const resendData = new FormData();
    resendData.append("email", email);
    resendData.append("password", password);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/resend`, {
        method: "PUT",
        body: resendData,
        credentials: 'include',
      });

      if (response.ok) {
        setError("Cod retrimis!");
      } else if (response.status === 400) {
        const errorMessage = await response.text();
        setError(extractTextFromHTML(errorMessage));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    const fetchProgrammes = async () => {
      try {
        const programmesData = await fetchProgrammesData();
        setProgrammes(programmesData);
      } catch (error) {
        console.error("Error fetching programmes:", error);
      }
    };
    fetchProgrammes();
  }, []);

  return (
    <>
      <div className={styles.mainContiner}>
        <Header />

        <div className={styles.wrapper}>
          {!showActivationForm ? (
            <div>
              <div className={styles.title}>Register</div>
              <form className={styles.form} onSubmit={handleRegister}>
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
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={styles.input}
                    type="password"
                    required
                  />
                  <label className={styles.label}>Password</label>
                </div>
                <div className={styles.field}>
                  <select
                    className={styles.select}
                    value={programmeId}
                    onChange={(e) => setProgrammeId(e.target.value)}
                  >
                    <option value="">Selecteaza o optiune</option>
                    {programmes.map((programme) => (
                      <option key={programme.id} value={programme.id}>
                        {programme.name}
                      </option>
                    ))}
                  </select>
                  <label className={styles.label}>Specializare</label>
                </div>
                {error && <div className={styles.errorContainer}>{error}</div>}
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="submit"
                    value="Inregistreaza-te"
                  />
                </div>
                <div className={styles.signupLink}>
                  Ai deja cont? <Link href="/userLogin">Conecteaza-te!</Link>
                </div>
              </form>
            </div>
          ) : (
            <div>
              <div className={styles.title}>Activare cont</div>
              <form className={styles.form} onSubmit={handleActivation}>
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    required
                  />
                  <label className={styles.label}>Activation Code</label>
                </div>
                <div className={styles.signupLink}>
                  <button className={styles.button} onClick={handleResendCode}>
                    Retrimitere cod
                  </button>
                </div>
                {error && <div className={styles.errorContainer}>{error}</div>}
                <div className={styles.field}>
                  <input
                    className={styles.input}
                    type="submit"
                    value="Activare"
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
