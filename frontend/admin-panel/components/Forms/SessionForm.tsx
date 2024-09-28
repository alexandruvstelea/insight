import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Session, Faculty, Room, Subject } from "@/utils/types";
import {
  weekTypeMapping,
  dayMapping,
  formatTimeForDisplay,
  formatTimeForBackend,
  sessionTypeMapping,
  startEndTimeOptions,
} from "@/utils/functions";
import ButtonGroup from "../ButtonGroup";
import { customSelectStyle } from "@/utils/customSelectStyle";
const SessionForm: React.FC<{
  isEditMode: boolean;
  session?: Session | null;
  faculties: Faculty[] | null | undefined;
  rooms: Room[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, session, rooms, faculties, onClose, onSubmit }) => {
  const [type, setType] = useState<string | null>(session?.type || null);
  const [selectedRoom, setSelectedRoom] = useState<number | null>(null);
  const [selectedFaculty, setSelectedFaculty] = useState<number | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [weekType, setWeekType] = useState<number | null>(null);
  const [start, setStart] = useState<string | null>(null);
  const [end, setEnd] = useState<string | null>(null);
  const [day, setDay] = useState<number | null>(null);

  const [subjectOptions, setSubjectOptions] = useState<
    { value: number; label: string }[]
  >([]);

  useEffect(() => {
    const fetchSubjects = async () => {
      if (selectedFaculty) {
        setSelectedSubject(null);

        try {
          const response = await fetch(
            `${process.env.API_URL}/subjects?faculty_id=${selectedFaculty}`
          );

          if (response.status === 404) {
            setSubjectOptions([]);
            console.warn(`No subjects found for faculty ID ${selectedFaculty}`);
            return;
          }
          if (!response.ok) {
            throw new Error("Failed to fetch subjects");
          }

          const data: Subject[] = await response.json();
          setSubjectOptions(
            data.map((subject) => ({
              value: subject.id,
              label: subject.name,
            }))
          );
        } catch (error) {
          console.error("Error fetching subjects:", error);
          setSubjectOptions([]);
        }
      } else {
        setSubjectOptions([]);
      }
    };

    fetchSubjects();
  }, [selectedFaculty]);

  useEffect(() => {
    if (session) {
      setType(session.type);
      setWeekType(session.week_type);
      setStart(formatTimeForDisplay(session.start));
      setEnd(formatTimeForDisplay(session.end));
      setDay(session.day);
      setSelectedRoom(session.room ? session.room.id : null);
      setSelectedFaculty(session.faculty_id[0]);
      const matchedSubject = session.subject
        ? subjectOptions.find((option) => option.value === session.subject.id)
        : null;
      if (matchedSubject) {
        setSelectedSubject(matchedSubject.value);
      } else {
        setSelectedSubject(null);
      }
    }
  }, [session, subjectOptions]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      type,
      room_id: selectedRoom,
      subject_id: selectedSubject,
      faculty_id: selectedFaculty,
      week_type: weekType,
      start: start ? formatTimeForBackend(start) : null,
      end: end ? formatTimeForBackend(end) : null,
      day,
    };
    console.log(payload);
    try {
      const url = isEditMode
        ? `${process.env.API_URL}/sessions/${session?.id}`
        : `${process.env.API_URL}/sessions`;
      const method = isEditMode ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (response.status === 409) {
        alert(`Intervalul noii sesiuni se suprapune cu unul existent.`);
        return;
      }

      if (!response.ok)
        throw new Error(
          isEditMode ? "Failed to edit session" : "Failed to add session"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting session:", error);
    }
  };

  const typeOptions = (
    Object.keys(sessionTypeMapping) as Array<keyof typeof sessionTypeMapping>
  ).map((key) => ({
    value: key,
    label: sessionTypeMapping[key],
  }));

  const weekTypeOptions = Object.keys(weekTypeMapping).map((key) => ({
    value: Number(key),
    label: weekTypeMapping[Number(key)],
  }));

  const filteredEndTimeOptions = start
    ? startEndTimeOptions.filter((option) => option.value > start)
    : startEndTimeOptions;

  const dayOptions = dayMapping.map((day, index) => ({
    value: index,
    label: day,
  }));

  const roomOptions = Array.isArray(rooms)
    ? rooms.map((room) => ({
        value: room.id,
        label: room.name,
      }))
    : [];

  const facultyOptions = Array.isArray(faculties)
    ? faculties.map((faculty) => ({
        value: faculty.id,
        label: faculty.name,
      }))
    : [];

  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded shadow-lg max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează sesiune" : "Adaugă sesiune"}
        </h3>
        <form onSubmit={handleSubmit}>
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
              styles={customSelectStyle}
              required
            />
          </div>
          <div className="mb-5">
            <label className="label">Curs *</label>
            <Select
              options={subjectOptions}
              value={
                subjectOptions.find(
                  (option) => option.value === selectedSubject
                ) || null
              }
              isSearchable
              onChange={(selectedOption) =>
                setSelectedSubject(selectedOption?.value || null)
              }
              styles={customSelectStyle}
              required
            />
          </div>
          <div className="mb-5">
            <label className="label">Sală *</label>
            <Select
              options={roomOptions}
              value={roomOptions.find(
                (option) => option.value === selectedRoom
              )}
              isSearchable
              onChange={(selectedOption) =>
                setSelectedRoom(selectedOption?.value || null)
              }
              styles={customSelectStyle}
              required
            />
          </div>
          <div className="mb-5">
            <label className="label">Tip *</label>
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
            <label className="label">Tipul săptămânii *</label>
            <Select
              options={weekTypeOptions}
              value={weekTypeOptions.find(
                (option) => option.value === weekType
              )}
              onChange={(selectedOption) =>
                setWeekType(selectedOption?.value || 0)
              }
              isSearchable={false}
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-5">
            <label className="label">Zi *</label>
            <Select
              options={dayOptions}
              value={dayOptions.find((option) => option.value === day)}
              onChange={(selectedOption) => setDay(selectedOption?.value || 0)}
              isSearchable={false}
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-5">
            <label className="label">Ora de început *</label>
            <Select
              options={startEndTimeOptions}
              value={startEndTimeOptions.find(
                (option) => option.value === start
              )}
              onChange={(selectedOption) => {
                setStart(selectedOption?.value || null);
                setEnd(null);
              }}
              required
              styles={customSelectStyle}
            />
          </div>

          <div className="mb-5">
            <label className="label">Ora de sfârșit *</label>
            <Select
              options={filteredEndTimeOptions}
              value={
                filteredEndTimeOptions.find((option) => option.value === end) ||
                null
              }
              onChange={(selectedOption) =>
                setEnd(selectedOption?.value || null)
              }
              required
              styles={customSelectStyle}
            />
          </div>

          <ButtonGroup onClose={onClose} isEditMode={isEditMode} />
        </form>
      </div>
    </div>
  );
};

export default SessionForm;
