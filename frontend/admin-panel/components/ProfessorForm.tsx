import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Professor, Faculty } from "@/utils/types";
import { genderOptions } from "@/utils/functions";
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
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">
          {isEditMode ? "Editează profesorul" : "Adaugă profesorul"}
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-1">Prenume</label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Numele de familie</label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Gen</label>
            <Select
              options={genderOptions}
              value={genderOptions.find((option) => option.value === gender)}
              onChange={(selectedOption) =>
                setGender(selectedOption?.value || "")
              }
              isSearchable={false}
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Facultăți</label>
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
              className="w-full"
            />
          </div>

          <div className="flex justify-between mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-500 text-white rounded"
            >
              Închide
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              {isEditMode ? "Editează" : "Adaugă"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfessorForm;
