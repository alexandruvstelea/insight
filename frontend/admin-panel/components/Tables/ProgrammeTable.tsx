"use client";

import ProgrammeForm from "@/components/Forms/ProgrammeForm";
import { useState, FC } from "react";
import { Programme, Subject } from "@/utils/types";
import Modal from "@/components/Modal";
import { ProgrammeTableProps } from "@/utils/interfaces";
import { programmeTypeMapping } from "@/utils/functions";
import TableActions from "@/components/TableActions";
import HeaderSection from "@/components/HeaderSection";
import SuccessToast from "@/components/SuccessToast";
import ErrorToast from "@/components/ErrorToast";

const ProgrammeTable: FC<ProgrammeTableProps> = ({
  programmes = [],
  faculties,
  subjects,
  fetchProgrammes,
}) => {
  const [isSubjectsModalOpen, setIsSubjectsModalOpen] = useState(false);
  const [selectedSubjects, setSelectedSubjects] = useState<Subject[]>([]);

  const [isAddProgrammeModalOpen, setIsAddProgrammeModalOpen] = useState(false);

  const [isEditProgrammeModalOpen, setIsEditProgrammeModalOpen] =
    useState(false);
  const [programmeToEdit, setProgrammeToEdit] = useState<Programme | null>(
    null
  );

  const [showSuccessToast, setShowSuccessToast] = useState(false);
  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleEdit = (programme: Programme) => {
    setProgrammeToEdit(programme);
    setIsEditProgrammeModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această specializare?")) {
      try {
        const response = await fetch(
          `${process.env.API_URL}/programmes/${id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error(`Eroare ${response.status}: ${response.statusText}`);
        }
        setShowSuccessToast(true);
        fetchProgrammes();
      } catch (error: any) {
        setErrorMessage(error.message);
        setShowErrorToast(true);
      }
    }
  };

  const handleShowSubjects = (subjects: Subject[]) => {
    setSelectedSubjects(subjects);
    setIsSubjectsModalOpen(true);
  };

  return (
    <>
      <div className=" p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="SPECIALIZĂRI"
          buttons={[
            {
              text: "ADAUGĂ SPECIALIZARE",
              onClick: () => setIsAddProgrammeModalOpen(true),
            },
          ]}
          count={programmes?.length || 0}
        />
        <table className="w-full text-base text-left text-gray-400">
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
                Studii universitare
              </th>
              <th scope="col" className="px-6 py-3">
                Facultate
              </th>
              <th scope="col" className="px-6 py-3">
                Cursuri
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(programmes) ? (
              programmes.map((programme) => (
                <tr
                  key={programme.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(programme.id)}
                    onEdit={() => handleEdit(programme)}
                    showEdit={true}
                  />
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {programme.name}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {programme.abbreviation}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {programmeTypeMapping[programme.type]}
                  </td>

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {programme.faculty ? programme.faculty.abbreviation : "-"}
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        programme.subjects.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        programme.subjects.length > 0 &&
                        handleShowSubjects(programme.subjects)
                      }
                      disabled={programme.subjects.length === 0}
                    >
                      Cursuri
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
                  Nu există specializări
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {(isEditProgrammeModalOpen || isAddProgrammeModalOpen) && (
        <ProgrammeForm
          isEditMode={isEditProgrammeModalOpen}
          programme={isEditProgrammeModalOpen ? programmeToEdit : null}
          faculties={faculties}
          subjects={subjects}
          onClose={() => {
            setIsEditProgrammeModalOpen(false);
            setIsAddProgrammeModalOpen(false);
          }}
          onSubmit={fetchProgrammes}
        />
      )}
      {isSubjectsModalOpen && (
        <Modal
          items={selectedSubjects}
          title="Cursuri"
          onClose={() => setIsSubjectsModalOpen(false)}
          renderItem={(subject) => (
            <>
              {subject.name} ({subject.abbreviation})
            </>
          )}
        />
      )}
      {showSuccessToast && (
        <SuccessToast
          message="Specializarea a fost ștearsă cu succes."
          onClose={() => setShowSuccessToast(false)}
        />
      )}

      {showErrorToast && (
        <ErrorToast
          message={errorMessage}
          onClose={() => setShowErrorToast(false)}
        />
      )}
    </>
  );
};

export default ProgrammeTable;
