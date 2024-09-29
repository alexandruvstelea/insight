import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Programme, Subject, Faculty } from "@/utils/types";
import { programmeTypeMapping } from "@/utils/functions";
import ButtonGroup from "../ButtonGroup";
import { customSelectStyle } from "@/utils/customSelectStyle";

const ProgrammeForm: React.FC<{
  isEditMode: boolean;
  programme?: Programme | null;
  faculties: Faculty[] | null | undefined;
  subjects: Subject[] | null | undefined;
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
      subjects: selectedSubjects,
    };
    console.log(payload);
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
        credentials: "include",
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

  const facultyOptions = Array.isArray(faculties)
    ? faculties.map((faculty) => ({
        value: faculty.id,
        label: faculty.name,
      }))
    : [];
  const subjectOptions = Array.isArray(subjects)
    ? subjects.map((subject) => ({
        value: subject.id,
        label: subject.name,
      }))
    : [];

  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează specializare" : "Adaugă specializare"}
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
            <label className="label">Tip Program *</label>
            <Select
              options={typeOptions}
              value={typeOptions.find((option) => option.value === type)}
              onChange={(selectedOption) =>
                setType(selectedOption?.value || "")
              }
              isSearchable={false}
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-5">
            <label className="label">Facultate *</label>
            <Select
              options={facultyOptions}
              value={facultyOptions.find(
                (option) => option.value === selectedFaculty
              )}
              isSearchable
              onChange={(selectedOption) =>
                setSelectedFaculty(selectedOption?.value || null)
              }
              required
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-5">
            <label className="label">Cursuri</label>
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
              styles={customSelectStyle}
            />
          </div>

          <ButtonGroup onClose={onClose} isEditMode={isEditMode} />
        </form>
      </div>
    </div>
  );
};

export default ProgrammeForm;
