import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Programme, Subject, Faculty } from "@/utils/types";
import { programmeTypeMapping } from "@/utils/functions";

const ProgrammeForm: React.FC<{
  isEditMode: boolean;
  programme?: Programme | null;
  faculties: Faculty[];
  subjects: Subject[];
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, programme, faculties, subjects, onClose, onSubmit }) => {
  const [name, setName] = useState(programme?.name || "");
  const [abbreviation, setAbbreviation] = useState(
    programme?.abbreviation || ""
  );
  const [type, setType] = useState(programme?.type || "");
  const [selectedFaculty, setSelectedFaculty] = useState<number | null>(null);
  const [selectedSubjects, setSelectedSubjects] = useState<number[]>([]);

  useEffect(() => {
    if (programme) {
      setSelectedFaculty(programme.faculty.id);
      setSelectedSubjects(programme.subjects.map((subject) => subject.id));
    }
  }, [programme]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      abbreviation,
      type,
      faculty_id: selectedFaculty,
      subjects: selectedSubjects.map(String),
    };
    try {
      const url = isEditMode
        ? `${process.env.API_URL}/programmes/${programme?.id}`
        : `${process.env.API_URL}/programmes`;
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
          isEditMode ? "Failed to edit programme" : "Failed to add programme"
        );

      const data = await response.json();

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting programme:", error);
    }
  };

  const typeOptions = (
    Object.keys(programmeTypeMapping) as Array<
      keyof typeof programmeTypeMapping
    >
  ).map((key) => ({
    value: key,
    label: programmeTypeMapping[key],
  }));

  const facultyOptions = faculties.map((faculty) => ({
    value: faculty.id,
    label: faculty.name,
  }));

  const subjectOptions = subjects.map((subject) => ({
    value: subject.id,
    label: subject.name,
  }));

  function setSelectedBuilding(arg0: number | null): void {
    throw new Error("Function not implemented.");
  }

  function setSelectedSessions(arg0: number[]): void {
    throw new Error("Function not implemented.");
  }

  return (
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">
          {isEditMode ? "Editează specializare" : "Adaugă specializare"}
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
            <label className="block mb-1">Tip Program</label>
            <Select
              options={typeOptions}
              value={typeOptions.find((option) => option.value === type)}
              onChange={(selectedOption) =>
                setType(selectedOption?.value || "")
              }
              isSearchable={false}
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Facultate</label>
            <Select
              options={facultyOptions}
              value={facultyOptions.find(
                (option) => option.value === selectedFaculty
              )}
              isSearchable
              onChange={(selectedOption) =>
                setSelectedFaculty(selectedOption?.value || null)
              }
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Cursuri</label>
            <Select
              options={subjectOptions}
              isMulti
              value={subjectOptions.filter((option) =>
                selectedSubjects.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedSubjects(
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

export default ProgrammeForm;
