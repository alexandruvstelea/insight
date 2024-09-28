"use client";

import { useState, FC } from "react";
import { Faculty, Building, Professor, Programme } from "@/utils/types";
import { FacultyTableProps } from "@/utils/interfaces";
import Modal from "@/components/Modal";
import FacultyForm from "@/components/Forms/FacultyForm";
import HeaderSection from "../HeaderSection";
import TableActions from "../TableActions";

const FacultyTable: FC<FacultyTableProps> = ({
  faculties = [],
  buildings,
  professors,
  programmes,
  fetchFaculties,
}) => {
  const [isProfessorsModalOpen, setIsProfessorsModalOpen] = useState(false);
  const [isBuildingsModalOpen, setIsBuildingsModalOpen] = useState(false);
  const [isProgrammesModalOpen, setIsProgrammesModalOpen] = useState(false);
  const [selectedProfessors, setSelectedProfessors] = useState<Professor[]>([]);
  const [selectedBuildings, setSelectedBuildings] = useState<Building[]>([]);
  const [selectedProgrammes, setSelectedProgrammes] = useState<Programme[]>([]);

  const [isAddFacultyModalOpen, setIsAddFacultyModalOpen] = useState(false);

  const [isEditFacultyModalOpen, setIsEditFacultyModalOpen] = useState(false);
  const [facultyToEdit, setFacultyToEdit] = useState<Faculty | null>(null);

  const handleEdit = (faculty: Faculty) => {
    setFacultyToEdit(faculty);
    setIsEditFacultyModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această facultate?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/faculties/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("An error occurred while deleting the faculty");
        }
        if (response.status == 200) {
          console.log("200");
        }

        fetchFaculties();
      } catch (error) {
        alert("A apărut o eroare la ștergerea facultății");
      }
    }
  };

  const handleShowProfessors = (professors: Professor[]) => {
    setSelectedProfessors(professors);
    setIsProfessorsModalOpen(true);
  };

  const handleShowBuildings = (buildings: Building[]) => {
    setSelectedBuildings(buildings);
    setIsBuildingsModalOpen(true);
  };

  const handleShowProgrammes = (programmes: Programme[]) => {
    setSelectedProgrammes(programmes);
    setIsProgrammesModalOpen(true);
  };

  return (
    <>
      <div className="  p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="FACULTĂȚI"
          buttons={[
            {
              text: "ADAUGĂ FACULTATE",
              onClick: () => setIsAddFacultyModalOpen(true),
            },
          ]}
          count={faculties?.length || 0}
        />

        <table className="w-full text-base text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr className="py-2">
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
                Clădiri
              </th>
              <th scope="col" className="px-6 py-3">
                Profesori
              </th>
              <th scope="col" className="px-6 py-3">
                Specializări
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(faculties) ? (
              faculties.map((faculty) => (
                <tr
                  key={faculty.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(faculty.id)}
                    onEdit={() => handleEdit(faculty)}
                    showEdit={true}
                  />
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {faculty.name}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {faculty.abbreviation}
                  </td>
                  <td scope="row" className="px-6 py-4 ">
                    <button
                      className={`${
                        faculty.buildings.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        faculty.buildings.length > 0 &&
                        handleShowBuildings(faculty.buildings)
                      }
                      disabled={faculty.buildings.length === 0}
                    >
                      Clădiri
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        faculty.professors.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        faculty.professors.length > 0 &&
                        handleShowProfessors(faculty.professors)
                      }
                      disabled={faculty.professors.length === 0}
                    >
                      Profesori
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4 ">
                    <button
                      className={`${
                        faculty.programmes.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        faculty.programmes.length > 0 &&
                        handleShowProgrammes(faculty.programmes)
                      }
                      disabled={faculty.programmes.length === 0}
                    >
                      Specializări
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={6}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există facultăți
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {(isEditFacultyModalOpen || isAddFacultyModalOpen) && (
        <FacultyForm
          isEditMode={isEditFacultyModalOpen}
          faculty={isEditFacultyModalOpen ? facultyToEdit : null}
          buildings={buildings}
          professors={professors}
          programmes={programmes}
          onClose={() => {
            setIsEditFacultyModalOpen(false);
            setIsAddFacultyModalOpen(false);
          }}
          onSubmit={fetchFaculties}
        />
      )}

      {isProfessorsModalOpen && (
        <Modal
          items={selectedProfessors}
          title="Profesori"
          onClose={() => setIsProfessorsModalOpen(false)}
          renderItem={(professor) => (
            <>
              {professor.first_name} {professor.last_name}
            </>
          )}
        />
      )}
      {isBuildingsModalOpen && (
        <Modal
          items={selectedBuildings}
          title="Clădiri"
          onClose={() => setIsBuildingsModalOpen(false)}
          renderItem={(building) => <>{building.name}</>}
        />
      )}
      {isProgrammesModalOpen && (
        <Modal
          items={selectedProgrammes}
          title="Specializări"
          onClose={() => setIsProgrammesModalOpen(false)}
          renderItem={(programme) => <>{programme.name}</>}
        />
      )}
    </>
  );
};

export default FacultyTable;
