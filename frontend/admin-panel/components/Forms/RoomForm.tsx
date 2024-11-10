import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Session, Room } from "@/utils/types";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
} from "@/utils/functions";
import ButtonGroup from "@/components/ButtonGroup";
import { customSelectStyle } from "@/utils/customSelectStyle";
const RoomForm: React.FC<{
  isEditMode: boolean;
  room?: Room | null;
  buildings: Building[] | null | undefined;
  sessions: Session[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, room, buildings, sessions, onClose, onSubmit }) => {
  const [name, setName] = useState(room?.name || "");
  const [uniqueCode, setUniqueCode] = useState(room?.unique_code || "");

  const [selectedBuilding, setSelectedBuilding] = useState<number | null>(null);
  const [selectedSessions, setSelectedSessions] = useState<number[]>([]);

  useEffect(() => {
    if (room) {
      setSelectedBuilding(room.building.id);
      setSelectedSessions(room.sessions.map((session) => session.id));
    }
  }, [room]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      unique_code: uniqueCode,
      building_id: selectedBuilding,
      sessions: selectedSessions,
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/rooms/${room?.id}`
        : `${process.env.API_URL}/rooms/`;
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
        alert(`Codul exista deja`);
        return;
      }

      if (!response.ok)
        throw new Error(
          isEditMode ? "Failed to edit room" : "Failed to add room"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting room:", error);
    }
  };

  const buildingOptions = Array.isArray(buildings)
    ? buildings.map((building) => ({
        value: building.id,
        label: building.name,
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

  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          {isEditMode ? "Editează cameră" : "Adaugă cameră"}
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
            <label htmlFor="uniqueCode" className="label">
              Id unic
            </label>
            <input
              id="uniqueCode"
              type="text"
              value={uniqueCode}
              onChange={(e) => setUniqueCode(e.target.value)}
              className="input"
            />
          </div>

          <div className="mb-5">
            <label className="label">Clădire *</label>
            <Select
              options={buildingOptions}
              value={buildingOptions.find(
                (option) => option.value === selectedBuilding
              )}
              isSearchable
              onChange={(selectedOption) =>
                setSelectedBuilding(selectedOption?.value || null)
              }
              styles={customSelectStyle}
              required
            />
          </div>

          <div className="mb-5">
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

export default RoomForm;
