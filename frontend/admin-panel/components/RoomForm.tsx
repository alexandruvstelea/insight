import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Session, Room } from "@/utils/types";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
} from "@/utils/functions";
const RoomForm: React.FC<{
  isEditMode: boolean;
  room?: Room | null;
  buildings: Building[];
  sessions: Session[];
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, room, buildings, sessions, onClose, onSubmit }) => {
  const [name, setName] = useState(room?.name || "");
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
      building_id: selectedBuilding,
      sessions: selectedSessions.map(String),
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/rooms/${room?.id}`
        : `${process.env.API_URL}/rooms`;
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
          isEditMode ? "Failed to edit room" : "Failed to add room"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting room:", error);
    }
  };

  const buildingOptions = buildings.map((building) => ({
    value: building.id,
    label: building.name,
  }));

  const sessionOptions = sessions.map((session) => ({
    value: session.id,
    label: `${session.start.slice(0, 5)} - ${session.end.slice(0, 5)} - ${
      sessionTypeMapping[session.type]
    } - Sem: ${session.semester} - ${weekTypeMapping[session.week_type]} - ${
      dayMapping[session.day]
    }`,
  }));

  return (
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">
          {isEditMode ? "Editează cameră" : "Adaugă cameră"}
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
            <label className="block mb-1">Clădire</label>
            <Select
              options={buildingOptions}
              value={buildingOptions.find(
                (option) => option.value === selectedBuilding
              )}
              isSearchable
              onChange={(selectedOption) =>
                setSelectedBuilding(selectedOption?.value || null)
              }
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1">Sesiuni</label>
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

export default RoomForm;
