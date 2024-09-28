"use client";

import { useState, FC } from "react";
import { Programme, Session, Subject } from "@/utils/types";
import { SubjectTableProps } from "@/utils/interfaces";
import Modal from "@/components/Modal";
import SubjectForm from "@/components/Forms/SubjectForm";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
} from "@/utils/functions";
import HeaderSection from "../HeaderSection";
import TableActions from "../TableActions";
const SubjectTable: FC<SubjectTableProps> = ({
  subjects = [],
  professors,
  programmes,
  sessions,
  fetchSubjects,
}) => {
  const [isProgrammesModalOpen, setIsProgrammesModalOpen] = useState(false);
  const [selectedProgrammes, setSelectedProgrammes] = useState<Programme[]>([]);

  const [isSessionsModalOpen, setIsSessionsModalOpen] = useState(false);
  const [selectedSessions, setSelectedSessions] = useState<Session[]>([]);

  const [isAddSubjectModalOpen, setIsAddSubjectModalOpen] = useState(false);

  const [isEditSubjectModalOpen, setIsEditSubjectModalOpen] = useState(false);
  const [subjectToEdit, setSubjectToEdit] = useState<Subject | null>(null);

  const handleEdit = (subject: Subject) => {
    setSubjectToEdit(subject);
    setIsEditSubjectModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această materie?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/subjects/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("An error occurred while deleting the subject");
        }

        fetchSubjects();
      } catch (error) {
        alert("A apărut o eroare la ștergerea materiei");
      }
    }
  };

  const handleShowSessions = (sessions: Session[]) => {
    setSelectedSessions(sessions);
    setIsSessionsModalOpen(true);
  };
  const handleShowProgrammes = (programmes: Programme[]) => {
    setSelectedProgrammes(programmes);
    setIsProgrammesModalOpen(true);
  };

  return (
    <>
      <div className="p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="MATERII"
          buttons={[
            {
              text: "ADAUGĂ MATERIE",
              onClick: () => setIsAddSubjectModalOpen(true),
            },
          ]}
          count={subjects?.length || 0}
        />
        <table className="w-full text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Nume
              </th>
              <th scope="col" className="px-6 py-3">
                Abreviere
              </th>
              <th scope="col" className="px-6 py-3">
                Semestru
              </th>
              <th scope="col" className="px-6 py-3">
                Profesor curs
              </th>
              <th scope="col" className="px-6 py-3">
                Profesor laborator
              </th>
              <th scope="col" className="px-6 py-3">
                Profesor seminar
              </th>
              <th scope="col" className="px-6 py-3">
                Profesor proiect
              </th>
              <th scope="col" className="px-6 py-3">
                Specializări
              </th>
              <th scope="col" className="px-6 py-3">
                Ore
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(subjects) ? (
              subjects.map((subject) => (
                <tr
                  key={subject.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(subject.id)}
                    onEdit={() => handleEdit(subject)}
                    showEdit={true}
                  />
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white "
                  >
                    {subject.name}
                  </td>

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.abbreviation}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.semester}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.course_professor
                      ? `${subject.course_professor.last_name} ${subject.course_professor.first_name}`
                      : "-"}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.laboratory_professor
                      ? `${subject.laboratory_professor.last_name} ${subject.laboratory_professor.first_name}`
                      : "-"}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.seminar_professor
                      ? `${subject.seminar_professor.last_name} ${subject.seminar_professor.first_name}`
                      : "-"}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {subject.project_professor
                      ? `${subject.project_professor.last_name} ${subject.project_professor.first_name}`
                      : "-"}
                  </td>

                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        subject.programmes.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        subject.programmes.length > 0 &&
                        handleShowProgrammes(subject.programmes)
                      }
                      disabled={subject.programmes.length === 0}
                    >
                      Specializări
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        subject.sessions.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        subject.sessions.length > 0 &&
                        handleShowSessions(subject.sessions)
                      }
                      disabled={subject.sessions.length === 0}
                    >
                      Ore
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={10}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există materii
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {(isEditSubjectModalOpen || isAddSubjectModalOpen) && (
        <SubjectForm
          isEditMode={isEditSubjectModalOpen}
          subject={isEditSubjectModalOpen ? subjectToEdit : null}
          programmes={programmes}
          sessions={sessions}
          professors={professors}
          onClose={() => {
            setIsEditSubjectModalOpen(false);
            setIsAddSubjectModalOpen(false);
          }}
          onSubmit={fetchSubjects}
        />
      )}
      {isSessionsModalOpen && (
        <Modal
          items={selectedSessions}
          title="Ore"
          onClose={() => setIsSessionsModalOpen(false)}
          isTable={true}
          renderItem={(session) => (
            <>
              <td>{`${session.start.slice(0, 5)}-${session.end.slice(
                0,
                5
              )}`}</td>
              <td>{dayMapping[session.day]}</td>
              <td>{sessionTypeMapping[session.type]}</td>
              <td>{session.semester}</td>
              <td>{weekTypeMapping[session.week_type]}</td>
            </>
          )}
        />
      )}
      {isProgrammesModalOpen && (
        <Modal
          items={selectedProgrammes}
          title="Specializări"
          onClose={() => setIsProgrammesModalOpen(false)}
          renderItem={(programme) => (
            <>{`${programme.name} (${programme.abbreviation})`}</>
          )}
        />
      )}
    </>
  );
};

export default SubjectTable;
