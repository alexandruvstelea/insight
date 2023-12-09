'use client'

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './page.module.css';
export default function AdminLogin() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const handleSubmit = async (e) => {

    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem('access_token', data.access_token);
        router.push("/adminLogin/adminPage");
      } else if (response.status === 401) {
        toast.error('Credențiale greșite. Te rog încearcă din nou.');
      } else {
        toast.error('A apărut o eroare la autentificare.');
      }
    } catch (err) {
      toast.error('A apărut o eroare la conectarea la server.');
    }
  };

  return (
    <>
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

        <form id={styles.loginAdmin} onSubmit={handleSubmit}>
          <div className={styles.adminTitle}>Admin Page</div>
          <div className={styles.inputs}>
            <label htmlFor="username">USERNAME</label>
            <input
              type="text"
              id="username"
              name="username"
              maxLength="20"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <label htmlFor="password">PASSWORD</label>
            <input
              type="password"
              id="password"
              name="password"
              maxLength="20"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">LOGIN</button>
          </div>
        </form>
      </div>
    </>
  );
};
