import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Building, Room, Faculty } from "@/utils/types";
import { customSelectStyle } from "@/utils/customSelectStyle";
import ButtonGroup from "@/components/ButtonGroup";
import { useNotification } from "@/context/NotificationContext";

const BuildingForm: React.FC<{
  isEditMode: boolean;
  building?: Building | null;
  rooms: Room[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  onClose: () => void;
  onSubmit: () => void;
}> = ({ isEditMode, building, rooms, faculties, onClose, onSubmit }) => {
  const { notify } = useNotification();
  const [name, setName] = useState(building?.name || "");
  const [latitude, setLatitude] = useState(building?.latitude || "");
  const [longitude, setLongitude] = useState(building?.longitude || "");

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
      latitude,
      longitude,
      rooms: selectedRooms,
      faculties: selectedFaculties,
    };

    try {
      const url = isEditMode
        ? `${process.env.API_URL}/buildings/${building?.id}`
        : `${process.env.API_URL}/buildings/`;
      const method = isEditMode ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Eroare ${response.status}: ${response.statusText}`);
      }

      notify(
        isEditMode
          ? "Clădirea a fost editată cu succes."
          : "Clădirea a fost adăugată cu succes.",
        "success"
      );
      onSubmit();
      onClose();
    } catch (error: any) {
      notify(error.message, "error");
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
    <>
      <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
        <div className="bg-slate-700 p-4 rounded  max-w-xl w-full max-h-[90vh] overflow-y-auto">
          <h3 className="text-xl font-semibold text-center mb-2 text-white">
            {isEditMode ? "Editează clădire" : "Adaugă clădire"}
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
              <label htmlFor="latitude" className="label">
                Latitudine *
              </label>
              <input
                id="latitude"
                type="number"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                className="input"
                required
              />
            </div>
            <div className="mb-5">
              <label htmlFor="longitude" className="label">
                Longitudine *
              </label>
              <input
                id="longitude"
                type="number"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                className="input"
                required
              />
            </div>

            <div className="mb-5">
              <label className="label">Săli</label>
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
                styles={customSelectStyle}
              />
            </div>

            <div className="mb-5">
              <label className="label">Facultăți</label>
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
                styles={customSelectStyle}
              />
            </div>
            <ButtonGroup onClose={onClose} isEditMode={isEditMode} />
          </form>
        </div>
      </div>
    </>
  );
};

export default BuildingForm;
