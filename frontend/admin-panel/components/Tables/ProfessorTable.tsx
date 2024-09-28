"use client";

import { useState, FC } from "react";
import { Faculty, Professor, SessionType } from "@/utils/types";
import { ProfessorTableProps } from "@/utils/interfaces";
import Modal from "@/components/Modal";
import { genderTypeMapping } from "@/utils/functions";
import ProfessorForm from "@/components/Forms/ProfessorForm";
import HeaderSection from "../HeaderSection";
import TableActions from "../TableActions";

const ProfessorTable: FC<ProfessorTableProps> = ({
  professors = [],
  faculties,
  fetchProfessors,
}) => {
  const [isFacultiesModalOpen, setIsFacultiesModalOpen] = useState(false);
  const [isCoursesModalOpen, setIsCoursesModalOpen] = useState(false);
  const [isLaboratoriesModalOpen, setIsLaboratoriesModalOpen] = useState(false);
  const [isSeminarsModalOpen, setIsSeminarsModalOpen] = useState(false);
  const [isProjectsModalOpen, setIsProjectsModalOpen] = useState(false);

  const [selectedFaculties, setSelectedFaculties] = useState<Faculty[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<SessionType[]>([]);
  const [selectedLaboratories, setSelectedLaboratories] = useState<
    SessionType[]
  >([]);
  const [selectedSeminars, setSelectedSeminars] = useState<SessionType[]>([]);
  const [selectedProjects, setSelectedProjects] = useState<SessionType[]>([]);

  const [isAddProfessorModalOpen, setIsAddProfessorModalOpen] = useState(false);

  const [isEditProfessorModalOpen, setIsEditProfessorModalOpen] =
    useState(false);
  const [professorToEdit, setProfessorToEdit] = useState<Professor | null>(
    null
  );

  const handleEdit = (professor: Professor) => {
    setProfessorToEdit(professor);
    setIsEditProfessorModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți aceast profesor?")) {
      try {
        const response = await fetch(
          `${process.env.API_URL}/professors/${id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error("An error occurred while deleting the professor");
        }

        fetchProfessors();
      } catch (error) {
        alert("A apărut o eroare la ștergerea profesorului");
      }
    }
  };

  const handleShowFaculties = (faculties: Faculty[]) => {
    setSelectedFaculties(faculties);
    setIsFacultiesModalOpen(true);
  };

  const handleShowCourses = (courses: SessionType[]) => {
    setSelectedCourses(courses);
    setIsCoursesModalOpen(true);
  };

  const handleShowLaboratories = (laboratories: SessionType[]) => {
    setSelectedLaboratories(laboratories);
    setIsLaboratoriesModalOpen(true);
  };

  const handleShowSeminars = (seminars: SessionType[]) => {
    setSelectedSeminars(seminars);
    setIsSeminarsModalOpen(true);
  };

  const handleShowProjects = (projects: SessionType[]) => {
    setSelectedProjects(projects);
    setIsProjectsModalOpen(true);
  };

  return (
    <>
      <div className=" p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="PROFESORI"
          buttons={[
            {
              text: "ADAUGĂ PROFESOR",
              onClick: () => setIsAddProfessorModalOpen(true),
            },
          ]}
          count={professors?.length || 0}
        />
        <table className="w-full text-base text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Prenume
              </th>
              <th scope="col" className="px-6 py-3">
                Familie
              </th>
              <th scope="col" className="px-6 py-3">
                Gen
              </th>
              <th scope="col" className="px-6 py-3">
                Facultăți
              </th>
              <th scope="col" className="px-6 py-3">
                Cursuri
              </th>
              <th scope="col" className="px-6 py-3">
                Laboratoare
              </th>
              <th scope="col" className="px-6 py-3">
                Seminarii
              </th>
              <th scope="col" className="px-6 py-3">
                Proiecte
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(professors) ? (
              professors.map((professor) => (
                <tr
                  key={professor.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(professor.id)}
                    onEdit={() => handleEdit(professor)}
                    showEdit={true}
                  />
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {professor.first_name}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {professor.last_name}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {genderTypeMapping[professor.gender]}
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        professor.faculties.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        professor.faculties.length > 0 &&
                        handleShowFaculties(professor.faculties)
                      }
                      disabled={professor.faculties.length === 0}
                    >
                      Facultăți
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        professor.courses.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        professor.courses.length > 0 &&
                        handleShowCourses(professor.courses)
                      }
                      disabled={professor.courses.length === 0}
                    >
                      Cursuri
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        professor.laboratories.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        professor.laboratories.length > 0 &&
                        handleShowLaboratories(professor.laboratories)
                      }
                      disabled={professor.laboratories.length === 0}
                    >
                      Laboratoare
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        professor.seminars.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        professor.seminars.length > 0 &&
                        handleShowSeminars(professor.seminars)
                      }
                      disabled={professor.seminars.length === 0}
                    >
                      Seminarii
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        professor.projects.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        professor.projects.length > 0 &&
                        handleShowProjects(professor.projects)
                      }
                      disabled={professor.projects.length === 0}
                    >
                      Proiecte
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={8}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există profesori
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {(isEditProfessorModalOpen || isAddProfessorModalOpen) && (
        <ProfessorForm
          isEditMode={isEditProfessorModalOpen}
          professor={isEditProfessorModalOpen ? professorToEdit : null}
          faculties={faculties}
          onClose={() => {
            setIsEditProfessorModalOpen(false);
            setIsAddProfessorModalOpen(false);
          }}
          onSubmit={fetchProfessors}
        />
      )}

      {isFacultiesModalOpen && (
        <Modal
          items={selectedFaculties}
          title="Facultăți"
          onClose={() => setIsFacultiesModalOpen(false)}
          renderItem={(faculty) => (
            <>
              {faculty.name} ({faculty.abbreviation})
            </>
          )}
        />
      )}
      {isCoursesModalOpen && (
        <Modal
          items={selectedCourses}
          title="Cursuri"
          onClose={() => setIsCoursesModalOpen(false)}
          renderItem={(course) => (
            <>
              {course.name} ({course.abbreviation})
            </>
          )}
        />
      )}
      {isLaboratoriesModalOpen && (
        <Modal
          items={selectedLaboratories}
          title="Laboratoare"
          onClose={() => setIsLaboratoriesModalOpen(false)}
          renderItem={(laboratorie) => (
            <>
              {laboratorie.name} ({laboratorie.abbreviation})
            </>
          )}
        />
      )}
      {isSeminarsModalOpen && (
        <Modal
          items={selectedSeminars}
          title="Laboratoare"
          onClose={() => setIsSeminarsModalOpen(false)}
          renderItem={(seminar) => (
            <>
              {seminar.name} ({seminar.abbreviation})
            </>
          )}
        />
      )}
      {isProjectsModalOpen && (
        <Modal
          items={selectedProjects}
          title="Laboratoare"
          onClose={() => setIsProjectsModalOpen(false)}
          renderItem={(project) => (
            <>
              {project.name} ({project.abbreviation})
            </>
          )}
        />
      )}
    </>
  );
};

export default ProfessorTable;
