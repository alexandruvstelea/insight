import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Room, Faculty } from "@/utils/types";

const BuildingForm: React.FC<{
  isEditMode: boolean;
  building?: Building | null;
  rooms: Room[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, building, rooms, faculties, onClose, onSubmit }) => {
  const [name, setName] = useState(building?.name || "");

  const [selectedRooms, setSelectedRooms] = useState<number[]>([]);
  const [selectedFaculties, setSelectedFaculties] = useState<number[]>([]);

  useEffect(() => {
    if (building) {
      setSelectedRooms(building.rooms.map((room) => room.id));

      setSelectedFaculties(building.faculties.map((faculty) => faculty.id));
    }
  }, [building]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      rooms: selectedRooms.map(String),
      faculties: selectedFaculties.map(String),
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/buildings/${building?.id}`
        : `${process.env.API_URL}/buildings`;
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
          isEditMode ? "Failed to edit building" : "Failed to add building"
        );

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting building:", error);
    }
  };

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
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">
          {isEditMode ? "Editează clădire" : "Adaugă clădire"}
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
            <label className="block mb-1">Săli</label>
            <Select
              options={roomOptions}
              isMulti
              value={roomOptions.filter((option) =>
                selectedRooms.includes(option.value)
              )}
              isSearchable
              onChange={(selectedOptions) =>
                setSelectedRooms(
                  selectedOptions.map(
                    (option: { value: number }) => option.value
                  )
                )
              }
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

export default BuildingForm;
