import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Professor, Programme, Faculty } from "@/utils/types";

const FacultyForm: React.FC<{
  isEditMode: boolean;
  faculty?: Faculty | null;
  buildings: Building[] | null | undefined;
  professors: Professor[] | null | undefined;
  programmes: Programme[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({
  isEditMode,
  faculty,
  buildings,
  professors,
  programmes,
  onClose,
  onSubmit,
}) => {
  const [name, setName] = useState(faculty?.name || "");
  const [abbreviation, setAbbreviation] = useState(faculty?.abbreviation || "");
  const [selectedBuildings, setSelectedBuildings] = useState<number[]>([]);
  const [selectedProfessors, setSelectedProfessors] = useState<number[]>([]);
  const [selectedProgrammes, setSelectedProgrammes] = useState<number[]>([]);

  useEffect(() => {
    if (faculty) {
      setSelectedBuildings(faculty.buildings.map((building) => building.id));

      setSelectedProfessors(
        faculty.professors.map((professor) => professor.id)
      );
      setSelectedProgrammes(
        faculty.programmes.map((programme) => programme.id)
      );
    }
  }, [faculty]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      abbreviation,
      buildings: selectedBuildings.map(String),
      professors: selectedProfessors.map(String),
      programmes: selectedProgrammes.map(String),
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/faculties/${faculty?.id}`
        : `${process.env.API_URL}/faculties`;
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
          isEditMode ? "Failed to edit faculty" : "Failed to add faculty"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting faculty:", error);
    }
  };

  const buildingOptions = Array.isArray(buildings)
    ? buildings.map((building) => ({
        value: building.id,
        label: building.name,
      }))
    : [];

  const professorOptions = Array.isArray(professors)
    ? professors.map((professor) => ({
        value: professor.id,
        label: `${professor.first_name} ${professor.last_name}`,
      }))
    : [];
  const programmeOptions = Array.isArray(programmes)
    ? programmes.map((programme) => ({
        value: programme.id,
        label: programme.name,
      }))
    : [];

  return (
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">
          {isEditMode ? "Editează facultate" : "Adaugă facultate"}
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-1">Nume</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Abreviere</label>
            <input
              type="text"
              value={abbreviation}
              onChange={(e) => setAbbreviation(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Clădiri</label>
            <Select
              options={buildingOptions}
              isMulti
              value={buildingOptions.filter((option) =>
                selectedBuildings.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedBuildings(
                  selectedOptions.map(
                    (option: { value: number }) => option.value
                  )
                )
              }
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Profesori</label>
            <Select
              options={professorOptions}
              isMulti
              value={professorOptions.filter((option) =>
                selectedProfessors.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedProfessors(
                  selectedOptions.map(
                    (option: { value: number }) => option.value
                  )
                )
              }
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Specializări</label>
            <Select
              options={programmeOptions}
              isMulti
              value={programmeOptions.filter((option) =>
                selectedProgrammes.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedProgrammes(
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

export default FacultyForm;
