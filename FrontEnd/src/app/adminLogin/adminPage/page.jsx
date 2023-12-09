'use client'
import React, { useState, useEffect } from 'react';
import styles from './page.module.css'
import Weeks from '@/components/admin/Weeks';
import Professors from '@/components/admin/Professors';
import Subjects from '@/components/admin/Subjects';
import Rooms from '@/components/admin/Rooms';
import Courses from '@/components/admin/Courses';
import useTokenCheck from '@/components/admin/useTokenCheck';
import { ToastContainer } from 'react-toastify';

export default function AdminPage() {
  const [weeks, setWeeks] = useState();
  const [professors, setProfessors] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [courses, setCourses] = useState();

  useTokenCheck();

  const fetchWeeks = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weeks`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setWeeks(data)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchProfessors = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/professors`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setProfessors(data);
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/subjects`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setSubjects(data)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchRooms = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setRooms(data)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/courses`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setCourses(data)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  useEffect(() => {
    fetchWeeks();
    fetchProfessors();
    fetchRooms();
    fetchSubjects();
    fetchCourses();
  }, []);

  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={10000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable={false}
        pauseOnHover
        theme="colored"
      />

      <div className={styles.tablesContainer} >
        <Weeks />
        <Professors professors={professors} fetchProfessors={fetchProfessors} />
        <Subjects professors={professors} subjects={subjects} fetchSubjects={fetchSubjects} />
        <Rooms rooms={rooms} fetchRooms={fetchRooms} />
        <Courses courses={courses} rooms={rooms} subjects={subjects} fetchCourses={fetchCourses} />
      </div>
    </>
  );
};