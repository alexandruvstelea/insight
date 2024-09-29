"use client";

import FacultyTable from "@/components/Tables/FacultyTable";
import RoomTable from "@/components/Tables/RoomTable";
import BuildingTable from "@/components/Tables/BuildingTable";
import ProgrammeTable from "@/components/Tables/ProgrammeTable";
import SessionTable from "@/components/Tables/SessionTable";
import ProfessorTable from "@/components/Tables/ProfessorTable";
import SubjectTable from "@/components/Tables/SubjectTable";
import WeekTable from "@/components/Tables/WeekTable";
import CommentTable from "@/components/Tables/CommentTable";
import UserTable from "@/components/Tables/UserTabel";

import { useEffect, useState } from "react";
import {
  Faculty,
  Room,
  Session,
  Building,
  Professor,
  Programme,
  Subject,
  Week,
  Comment,
  User,
} from "@/utils/types";
import MenuItem from "./MenuItem";
import ReportForm from "./Forms/ReportForm";
import InfoTab from "./InfoTab";

export default function Desboard(): JSX.Element {
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [programmes, setProgrammes] = useState<Programme[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [weeks, setWeeks] = useState<Week[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  const [isOpen, setIsOpen] = useState(true);
  const [showList, setShowList] = useState(true);

  const [openTable, setOpenTable] = useState<string | null>("info");
  const [activeTable, setActiveTable] = useState<string | null>(null);

  const fetchData = async (
    url: string,
    setState: React.Dispatch<React.SetStateAction<any[]>>
  ) => {
    try {
      const response = await fetch(url, {
        cache: "no-store",
        credentials: "include",
      });

      if (!response.ok) {
        if (response.status === 404) {
          setState([]);
          console.warn(`No data found at ${url} (404)`);
        } else {
          throw new Error(`Request failed with status ${response.status}`);
        }
        return;
      }

      const data = await response.json();
      setState(data);
    } catch (error) {
      console.error(`Error fetching data from ${url}:`, error);
    }
  };

  const handleTableToggle = (tableName: string) => {
    if (openTable === tableName) {
      setOpenTable("info");
      setActiveTable(null);
    } else {
      setOpenTable(tableName);
      setActiveTable(tableName);
    }
  };

  const toggleDrawer = () => setIsOpen(!isOpen);

  useEffect(() => {
    if (!isOpen) {
      const timer = setTimeout(() => {
        setShowList(false);
      }, 300);
      return () => clearTimeout(timer);
    } else {
      setShowList(true);
    }
  }, [isOpen]);

  useEffect(() => {
    const fetchInitialData = async () => {
      await Promise.all([
        fetchData(`${process.env.API_URL}/weeks`, setWeeks),
        fetchData(`${process.env.API_URL}/faculties`, setFaculties),
        fetchData(`${process.env.API_URL}/buildings`, setBuildings),
        fetchData(`${process.env.API_URL}/rooms`, setRooms),
        fetchData(`${process.env.API_URL}/programmes`, setProgrammes),
        fetchData(`${process.env.API_URL}/professors`, setProfessors),
        fetchData(`${process.env.API_URL}/subjects`, setSubjects),
        fetchData(`${process.env.API_URL}/sessions`, setSessions),
        fetchData(`${process.env.API_URL}/comments`, setComments),
        fetchData(`${process.env.API_URL}/users`, setUsers),
      ]);
    };
    fetchInitialData();
  }, []);

  useEffect(() => {
    if (openTable === "faculties")
      fetchData(`${process.env.API_URL}/faculties`, setFaculties);
    if (openTable === "buildings")
      fetchData(`${process.env.API_URL}/buildings`, setBuildings);
    if (openTable === "professors")
      fetchData(`${process.env.API_URL}/professors`, setProfessors);
    if (openTable === "programmes")
      fetchData(`${process.env.API_URL}/programmes`, setProgrammes);
    if (openTable === "rooms")
      fetchData(`${process.env.API_URL}/rooms`, setRooms);
    if (openTable === "sessions")
      fetchData(`${process.env.API_URL}/sessions`, setSessions);
    if (openTable === "subjects")
      fetchData(`${process.env.API_URL}/subjects`, setSubjects);
    if (openTable === "weeks")
      fetchData(`${process.env.API_URL}/weeks`, setWeeks);
    if (openTable === "comments")
      fetchData(`${process.env.API_URL}/comments`, setComments);
    if (openTable === "users")
      fetchData(`${process.env.API_URL}/users`, setUsers);
  }, [openTable]);

  return (
    <>
      <div
        className={`fixed top-0 left-0 z-40 w-64 h-screen p-4 rounded-r-xl overflow-y-auto transition-transform duration-300  ${
          isOpen ? "translate-x-0" : "-translate-x-[80%]"
        }  bg-gray-800`}
        tabIndex={-1}
      >
        <h5
          className={`text-base font-semibold uppercase text-gray-400 ${
            showList ? "block" : "hidden"
          }`}
        >
          Meniu
        </h5>
        <button
          type="button"
          onClick={toggleDrawer}
          className="rounded-lg p-1.5 absolute top-2.5 end-2.5 transition duration-300 hover:bg-gray-600 "
        >
          <img src="/svgs/menu.svg" className="w-auto  h-6" alt="Menu" />
        </button>
        <div className="py-4 overflow-y-auto">
          <ul className={`space-y-2 ${showList ? "block" : "hidden"}`}>
            <MenuItem
              label="Săptămâni"
              isActive={activeTable === "weeks"}
              onClick={() => handleTableToggle("weeks")}
            />
            <MenuItem
              label="Facultăți"
              isActive={activeTable === "faculties"}
              onClick={() => handleTableToggle("faculties")}
            />
            <MenuItem
              label="Clădiri"
              isActive={activeTable === "buildings"}
              onClick={() => handleTableToggle("buildings")}
            />
            <MenuItem
              label="Săli"
              isActive={activeTable === "rooms"}
              onClick={() => handleTableToggle("rooms")}
            />
            <MenuItem
              label="Specializări"
              isActive={activeTable === "programmes"}
              onClick={() => handleTableToggle("programmes")}
            />
            <MenuItem
              label="Profesori"
              isActive={activeTable === "professors"}
              onClick={() => handleTableToggle("professors")}
            />
            <MenuItem
              label="Materii"
              isActive={activeTable === "subjects"}
              onClick={() => handleTableToggle("subjects")}
            />
            <MenuItem
              label="Ore"
              isActive={activeTable === "sessions"}
              onClick={() => handleTableToggle("sessions")}
            />
            <MenuItem
              label="Comentarii"
              isActive={activeTable === "comments"}
              onClick={() => handleTableToggle("comments")}
            />
            <MenuItem
              label="Users"
              isActive={activeTable === "users"}
              onClick={() => handleTableToggle("users")}
            />
          </ul>
          <button
            type="button"
            onClick={() => handleTableToggle("bugReport")}
            className={`rounded-lg p-1.5 absolute bottom-2.5 start-2 transition duration-300 hover:bg-gray-600 ${
              activeTable === "bugReport"
                ? "bg-gray-600 text-white"
                : "text-white"
            }`}
          >
            <img src="/svgs/flag.svg" className="w-auto h-6" alt="Bag report" />
          </button>
        </div>

        <button
          type="button"
          onClick={() => handleTableToggle("info")}
          className={
            "rounded-lg p-1.5 absolute bottom-2.5 end-2 transition duration-300 hover:bg-gray-600 "
          }
        >
          <img src="/svgs/info.svg" className="w-auto  h-6" alt="Info" />
        </button>
      </div>

      <div
        className={`transition-all ease-in-out duration-300 ${
          isOpen ? "ml-64" : "ml-12"
        } p-4`}
      >
        {openTable === "info" && <InfoTab />}
        {openTable === "bugReport" && <ReportForm />}

        {openTable === "weeks" && (
          <WeekTable
            weeks={weeks}
            fetchWeeks={() =>
              fetchData(`${process.env.API_URL}/weeks`, setWeeks)
            }
          />
        )}

        {openTable === "faculties" && (
          <FacultyTable
            faculties={faculties}
            buildings={buildings}
            professors={professors}
            programmes={programmes}
            fetchFaculties={() =>
              fetchData(`${process.env.API_URL}/faculties`, setFaculties)
            }
          />
        )}
        {openTable === "buildings" && (
          <BuildingTable
            buildings={buildings}
            rooms={rooms}
            faculties={faculties}
            fetchBuildings={() =>
              fetchData(`${process.env.API_URL}/buildings`, setBuildings)
            }
          />
        )}
        {openTable === "rooms" && (
          <RoomTable
            rooms={rooms}
            sessions={sessions}
            buildings={buildings}
            fetchRooms={() =>
              fetchData(`${process.env.API_URL}/rooms`, setRooms)
            }
          />
        )}
        {openTable === "programmes" && (
          <ProgrammeTable
            programmes={programmes}
            faculties={faculties}
            subjects={subjects}
            fetchProgrammes={() =>
              fetchData(`${process.env.API_URL}/programmes`, setProgrammes)
            }
          />
        )}
        {openTable === "professors" && (
          <ProfessorTable
            professors={professors}
            faculties={faculties}
            fetchProfessors={() =>
              fetchData(`${process.env.API_URL}/professors`, setProfessors)
            }
          />
        )}
        {openTable === "subjects" && (
          <SubjectTable
            subjects={subjects}
            programmes={programmes}
            sessions={sessions}
            professors={professors}
            fetchSubjects={() =>
              fetchData(`${process.env.API_URL}/subjects`, setSubjects)
            }
          />
        )}
        {openTable === "sessions" && (
          <SessionTable
            sessions={sessions}
            rooms={rooms}
            faculties={faculties}
            subjects={subjects}
            fetchSessions={() =>
              fetchData(`${process.env.API_URL}/sessions`, setSessions)
            }
          />
        )}
        {openTable === "comments" && (
          <CommentTable
            comments={comments}
            fetchComments={() =>
              fetchData(`${process.env.API_URL}/comments`, setComments)
            }
          />
        )}
        {openTable === "users" && (
          <UserTable
            users={users}
            fetchUsers={() =>
              fetchData(`${process.env.API_URL}/users`, setUsers)
            }
          />
        )}
      </div>
    </>
  );
}
