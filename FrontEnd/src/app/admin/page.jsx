"use client";
import React, { useState, useEffect } from "react";
import styles from "./page.module.css";
import Weeks from "@/components/admin/Weeks";
import Professors from "@/components/admin/Professors";
import Subjects from "@/components/admin/Subjects";
import Programmes from "@/components/admin/Programmes";
import Rooms from "@/components/admin/Rooms";
import Courses from "@/components/admin/Courses";
import Comments from "@/components/admin/Comments";
import Button from "@mui/joy/Button";
import { ToastContainer } from "react-toastify";
import { fetchCheckLogin } from "@/app/Actions/getUserData";
import { useRouter } from "next/navigation";

export default function Admin() {
  const router = useRouter();

  useEffect(() => {
    const checkLoggedIn = async () => {
      try {
        const user = await fetchCheckLogin();
        if (!user.logged_in || user.type != 0) {
          router.push("/login");
        }
      } catch (error) {
        console.error("Error checking login status:", error);
      }
    };

    checkLoggedIn();
  }, [router]);

  const [weeks, setWeeks] = useState();
  const [professors, setProfessors] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [courses, setCourses] = useState();
  const [comments, setComments] = useState();
  const [programmes, setProgrammes] = useState();

  const fetchWeeks = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weeks`);
      if (!response.ok) {
        if (response.status === 404) {
          setWeeks([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      setWeeks(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const fetchProfessors = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/professors`
      );
      if (!response.ok) {
        if (response.status === 404) {
          setProfessors([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      setProfessors(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/subjects`);
      if (!response.ok) {
        if (response.status === 404) {
          setSubjects([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      setSubjects(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const fetchRooms = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms`);
      if (!response.ok) {
        if (response.status === 404) {
          setRooms([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }
      const data = await response.json();
      setRooms(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/courses`);
      if (!response.ok) {
        if (response.status === 404) {
          setCourses([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }

      const data = await response.json();
      setCourses(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };
  const fetchCommnets = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/comments`);
      if (!response.ok) {
        if (response.status === 404) {
          setComments([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }

      const data = await response.json();
      setComments(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };
  const fetchProgrammes = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/programmes`
      );
      if (!response.ok) {
        if (response.status === 404) {
          setProgrammes([]);
        } else {
          throw new Error("Failed to fetch");
        }
      }

      const data = await response.json();
      setProgrammes(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  useEffect(() => {
    fetchWeeks();
    fetchProfessors();
    fetchRooms();
    fetchSubjects();
    fetchCourses();
    fetchCommnets();
    fetchProgrammes();
  }, []);

  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={4500}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable={false}
        pauseOnHover
        theme="colored"
      />

      <div className={styles.tablesContainer}>
        <Button
          component="a"
          href="/"
          size="lg"
          sx={{
            width: "32rem",
            margin: "2rem 0",
            fontSize: "1.5rem",
            fontFamily: "inherit",
          }}
        >
          Către Pagina Principală
        </Button>
        <Weeks weeks={weeks} fetchWeeks={fetchWeeks} />
        <Professors professors={professors} fetchProfessors={fetchProfessors} />
        <Subjects
          professors={professors}
          subjects={subjects}
          fetchSubjects={fetchSubjects}
        />
        <Rooms rooms={rooms} fetchRooms={fetchRooms} />
        <Programmes programmes={programmes} fetchProgrammes={fetchProgrammes} />
        <Courses
          courses={courses}
          rooms={rooms}
          subjects={subjects}
          fetchCourses={fetchCourses}
        />
        <Comments comments={comments} fetchCommnets={fetchCommnets} />
        <Button
          component="a"
          href="/"
          size="lg"
          sx={{
            width: "32rem",
            margin: "0 0 3.5rem 0",
            fontSize: "1.5rem",
            fontFamily: "inherit",
          }}
        >
          Către Pagina Principală
        </Button>
      </div>
    </>
  );
}
