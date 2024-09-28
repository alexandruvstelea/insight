"use client";

import HeaderSection from "@/components/HeaderSection";
import { useState, FC } from "react";
import { Faculty, Room, Building } from "@/utils/types";
import Modal from "@/components/Modal";
import BuildingForm from "@/components/Forms/BuildingForm";
import { BuildingTableProps } from "@/utils/interfaces";
import TableActions from "../TableActions";

const BuildingTable: FC<BuildingTableProps> = ({
  buildings = [],
  rooms,
  faculties,
  fetchBuildings,
}) => {
  const [isRoomsModalOpen, setIsRoomsModalOpen] = useState(false);
  const [isFacultiesModalOpen, setIsFacultiesModalOpen] = useState(false);

  const [selectedRooms, setSelectedRooms] = useState<Room[]>([]);
  const [selectedFaculties, setSelectedFaculties] = useState<Faculty[]>([]);

  const [isAddBuildingModalOpen, setIsAddBuildingModalOpen] = useState(false);
  const [isEditBuildingModalOpen, setIsEditBuildingModalOpen] = useState(false);

  const [buildingToEdit, setBuildingToEdit] = useState<Building | null>(null);

  const handleEdit = (building: Building) => {
    setBuildingToEdit(building);
    setIsEditBuildingModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această clădire?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/buildings/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("An error occurred while deleting the building");
        }
        fetchBuildings();
      } catch (error) {
        alert("A apărut o eroare la ștergerea clădirii");
      }
    }
  };

  const handleShowRooms = (rooms: Room[]) => {
    setSelectedRooms(rooms);
    setIsRoomsModalOpen(true);
  };

  const handleShowFaculties = (faculties: Faculty[]) => {
    setSelectedFaculties(faculties);
    setIsFacultiesModalOpen(true);
  };
  return (
    <>
      <div className=" p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="CLĂDIRI"
          buttons={[
            {
              text: "ADAUGĂ CLĂDIRE",
              onClick: () => setIsAddBuildingModalOpen(true),
            },
          ]}
          count={buildings?.length || 0}
        />

        <table className="w-full text-base text-left text-gray-400">
          <thead className=" text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Nume
              </th>
              <th scope="col" className="px-6 py-3">
                Săli
              </th>
              <th scope="col" className="px-6 py-3">
                Facultăți
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(buildings) ? (
              buildings.map((building) => (
                <tr
                  key={building.id}
                  className=" border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(building.id)}
                    onEdit={() => handleEdit(building)}
                    showEdit={true}
                  />

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {building.name}
                  </td>

                  <td scope="row" className="px-6 py-4  ">
                    <button
                      className={`${
                        building.rooms.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        building.rooms.length > 0 &&
                        handleShowRooms(building.rooms)
                      }
                      disabled={building.rooms.length === 0}
                    >
                      Săli
                    </button>
                  </td>
                  <td scope="row" className="px-6 py-4 ">
                    <button
                      className={`${
                        building.faculties.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        building.faculties.length > 0 &&
                        handleShowFaculties(building.faculties)
                      }
                      disabled={building.faculties.length === 0}
                    >
                      Facultăți
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={4}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există clădiri
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {(isEditBuildingModalOpen || isAddBuildingModalOpen) && (
        <BuildingForm
          isEditMode={isEditBuildingModalOpen}
          building={isEditBuildingModalOpen ? buildingToEdit : null}
          rooms={rooms}
          faculties={faculties}
          onClose={() => {
            setIsEditBuildingModalOpen(false);
            setIsAddBuildingModalOpen(false);
          }}
          onSubmit={fetchBuildings}
        />
      )}

      {isRoomsModalOpen && (
        <Modal
          items={selectedRooms}
          title="Săli"
          onClose={() => setIsRoomsModalOpen(false)}
          renderItem={(room) => <>{room.name}</>}
        />
      )}
      {isFacultiesModalOpen && (
        <Modal
          items={selectedFaculties}
          title="Facultăți"
          onClose={() => setIsFacultiesModalOpen(false)}
          renderItem={(faculty) => <>{faculty.name}</>}
        />
      )}
    </>
  );
};

export default BuildingTable;
