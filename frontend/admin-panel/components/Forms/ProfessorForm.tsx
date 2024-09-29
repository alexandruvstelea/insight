import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Professor, Faculty } from "@/utils/types";
import { genderOptions } from "@/utils/functions";
import ButtonGroup from "../ButtonGroup";
import { customSelectStyle } from "@/utils/customSelectStyle";
const ProfessorForm: React.FC<{
  isEditMode: boolean;
  professor?: Professor | null;
  faculties: Faculty[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, professor, faculties, onClose, onSubmit }) => {
  const [firstName, setFirstName] = useState(professor?.first_name || "");
  const [lastName, setLastName] = useState(professor?.last_name || "");
  const [gender, setGender] = useState(professor?.gender || "");
  const [selectedFaculties, setSelectedFaculties] = useState<number[]>([]);

  useEffect(() => {
    if (professor) {
      setSelectedFaculties(professor.faculties.map((faculty) => faculty.id));
      setGender(professor.gender);
    }
  }, [professor]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      first_name: firstName,
      last_name: lastName,
      gender,
      faculties: selectedFaculties.map(String),
    };
    try {
      const url = isEditMode
        ? `${process.env.API_URL}/professors/${professor?.id}`
        : `${process.env.API_URL}/professors`;
      const method = isEditMode ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!response.ok)
        throw new Error(
          isEditMode ? "Failed to edit professor" : "Failed to add professor"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting professor:", error);
    }
  };

  const facultyOptions = Array.isArray(faculties)
    ? faculties.map((faculty) => ({
        value: faculty.id,
        label: faculty.name,
      }))
    : [];

  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează profesorul" : "Adaugă profesorul"}
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label htmlFor="firstName" className="label">
              Prenume *
            </label>
            <input
              id="firstName"
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="input"
              required
            />
          </div>
          <div className="mb-5">
            <label htmlFor="lastName" className="label">
              Numele de familie *
            </label>
            <input
              id="lastName"
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="input"
              required
            />
          </div>
          <div className="mb-5">
            <label className="label">Gen *</label>
            <Select
              options={genderOptions}
              value={genderOptions.find((option) => option.value === gender)}
              onChange={(selectedOption) =>
                setGender(selectedOption?.value || "")
              }
              isSearchable={false}
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-5">
            <label className="label">Facultăți</label>
            <Select
              options={facultyOptions}
              isMulti
              value={facultyOptions.filter((option) =>
                selectedFaculties.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedFaculties(
                  selectedOptions.map(
                    (option: { value: number }) => option.value
                  )
                )
              }
              styles={customSelectStyle}
            />
          </div>

          <ButtonGroup onClose={onClose} isEditMode={isEditMode} />
        </form>
      </div>
    </div>
  );
};

export default ProfessorForm;
