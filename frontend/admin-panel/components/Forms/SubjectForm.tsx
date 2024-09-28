import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Subject, Programme, Session, Professor } from "@/utils/types";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
  semesterOptions,
} from "@/utils/functions";
import ButtonGroup from "../ButtonGroup";
import { customSelectStyle } from "@/utils/customSelectStyle";
const SubjectForm: React.FC<{
  isEditMode: boolean;
  subject?: Subject | null;
  programmes: Programme[] | null | undefined;
  sessions: Session[] | null | undefined;
  professors: Professor[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({
  isEditMode,
  subject,
  programmes,
  sessions,
  professors,
  onClose,
  onSubmit,
}) => {
  const [name, setName] = useState(subject?.name || "");
  const [abbreviation, setAbbreviation] = useState(subject?.abbreviation || "");

  const [semester, setSemester] = useState<number | null>(
    subject?.semester ?? null
  );
  const [courseProfessor, setCourseProfessor] = useState<number | null>(null);
  const [laboratoryProfessor, setLaboratoryProfessor] = useState<number | null>(
    null
  );
  const [seminarProfessor, setSeminarProfessor] = useState<number | null>(null);
  const [projectProfessor, setProjectProfessor] = useState<number | null>(null);
  const [selectedProgrammes, setSelectedProgrammes] = useState<number[]>([]);
  const [selectedSessions, setSelectedSessions] = useState<number[]>([]);

  useEffect(() => {
    if (subject) {
      setCourseProfessor(subject.course_professor_id || null);
      setLaboratoryProfessor(subject.laboratory_professor_id || null);
      setSeminarProfessor(subject.seminar_professor_id || null);
      setProjectProfessor(subject.project_professor_id || null);
      setSelectedProgrammes(
        subject.programmes.map((programme) => programme.id)
      );
      setSelectedSessions(subject.sessions.map((session) => session.id));
    }
  }, [subject]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      abbreviation,
      semester: Number(semester),
      course_professor_id: courseProfessor,
      laboratory_professor_id: laboratoryProfessor,
      seminar_professor_id: seminarProfessor,
      project_professor_id: projectProfessor,
      programmes: selectedProgrammes,
      sessions: selectedSessions,
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/subjects/${subject?.id}`
        : `${process.env.API_URL}/subjects`;
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
          isEditMode ? "Failed to edit subject" : "Failed to add subject"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting subject:", error);
    }
  };

  const programmeOptions = Array.isArray(programmes)
    ? programmes.map((programme) => ({
        value: programme.id,
        label: programme.name,
      }))
    : [];

  const sessionOptions = Array.isArray(sessions)
    ? sessions.map((session) => ({
        value: session.id,
        label: `${session.start.slice(0, 5)} - ${session.end.slice(0, 5)} - ${
          sessionTypeMapping[session.type]
        } - Sem: ${session.semester} - ${
          weekTypeMapping[session.week_type]
        } - ${dayMapping[session.day]}`,
      }))
    : [];

  const professorOptions = Array.isArray(professors)
    ? professors.map((professor) => ({
        value: professor.id,
        label: `${professor.first_name} ${professor.last_name}`,
      }))
    : [];

  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded shadow-lg max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează materie" : "Adaugă materie"}
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
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
          <div className="mb-4">
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
          <div className="mb-4">
            <label className="label">Semestru *</label>
            <Select
              options={semesterOptions}
              value={semesterOptions.find(
                (option) => option.value === semester
              )}
              onChange={(selectedOption) => {
                if (selectedOption) {
                  setSemester(selectedOption.value);
                }
              }}
              isSearchable={false}
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-4">
            <label className="label">Profesor Curs</label>
            <Select
              options={professorOptions}
              value={professorOptions.find(
                (option) => option.value === courseProfessor
              )}
              onChange={(selectedOption) =>
                setCourseProfessor(selectedOption?.value || null)
              }
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-4">
            <label className="label">Profesor Laborator</label>
            <Select
              options={professorOptions}
              value={professorOptions.find(
                (option) => option.value === laboratoryProfessor
              )}
              onChange={(selectedOption) =>
                setLaboratoryProfessor(selectedOption?.value || null)
              }
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-4">
            <label className="label">Profesor Seminar</label>
            <Select
              options={professorOptions}
              value={professorOptions.find(
                (option) => option.value === seminarProfessor
              )}
              onChange={(selectedOption) =>
                setSeminarProfessor(selectedOption?.value || null)
              }
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-4">
            <label className="label">Profesor Proiect</label>
            <Select
              options={professorOptions}
              value={professorOptions.find(
                (option) => option.value === projectProfessor
              )}
              onChange={(selectedOption) =>
                setProjectProfessor(selectedOption?.value || null)
              }
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-4">
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

          <div className="mb-4">
            <label className="label">Sesiuni</label>
            <Select
              options={sessionOptions}
              isMulti
              value={sessionOptions.filter((option) =>
                selectedSessions.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedSessions(
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

export default SubjectForm;
