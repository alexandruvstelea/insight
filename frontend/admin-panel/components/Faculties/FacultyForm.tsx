import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Professor, Programme, Faculty } from "@/utils/types";
import { customSelectStyle } from "@/utils/customSelectStyle";
import ButtonGroup from "../ButtonGroup";
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
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded shadow-lg max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează facultate" : "Adaugă facultate"}
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label htmlFor="name" className="label">
              Nume *
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
              required
            />
          </div>
          <div className="mb-5">
            <label htmlFor="abbreviation" className="label">
              Abreviere *
            </label>
            <input
              id="abbreviation"
              type="text"
              value={abbreviation}
              onChange={(e) => setAbbreviation(e.target.value)}
              className="input"
              required
            />
          </div>

          <div className="mb-5">
            <label className="label">Clădiri</label>
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
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-5">
            <label className="label">Profesori</label>
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
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-5">
            <label className="label">Specializări</label>
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
              styles={customSelectStyle}
            />
          </div>

          <ButtonGroup onClose={onClose} isEditMode={isEditMode} />
        </form>
      </div>
    </div>
  );
};

export default FacultyForm;
