"use client";

import RoomForm from "@/components/Forms/RoomForm";
import { useState, FC } from "react";
import { Room, Session } from "@/utils/types";
import Modal from "@/components/Modal";
import { RoomTableProps } from "@/utils/interfaces";
import SuccessToast from "@/components/SuccessToast";
import ErrorToast from "@/components/ErrorToast";
import TableActions from "@/components/TableActions";
import HeaderSection from "@/components/HeaderSection";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
} from "@/utils/functions";

const RoomTable: FC<RoomTableProps> = ({
  rooms = [],
  buildings,
  sessions,
  fetchRooms,
}) => {
  const [isSessionsModalOpen, setIsSessionsModalOpen] = useState(false);
  const [selectedSessions, setSelectedSessions] = useState<Session[]>([]);

  const [isAddRoomModalOpen, setIsAddRoomModalOpen] = useState(false);

  const [isEditRoomModalOpen, setIsEditRoomModalOpen] = useState(false);
  const [roomToEdit, setRoomToEdit] = useState<Room | null>(null);

  const [showSuccessToast, setShowSuccessToast] = useState(false);
  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleEdit = (room: Room) => {
    setRoomToEdit(room);
    setIsEditRoomModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această sală?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/rooms/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Eroare ${response.status}: ${response.statusText}`);
        }
        setShowSuccessToast(true);
        fetchRooms();
      } catch (error: any) {
        setErrorMessage(error.message);
        setShowErrorToast(true);
      }
    }
  };

  const handleShowSessions = (sessions: Session[]) => {
    setSelectedSessions(sessions);
    setIsSessionsModalOpen(true);
  };

  return (
    <>
      <div className="p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="SĂLI"
          buttons={[
            {
              text: "ADAUGĂ SALĂ",
              onClick: () => setIsAddRoomModalOpen(true),
            },
          ]}
          count={rooms?.length || 0}
        />
        <table className="w-full text-base text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Nume
              </th>
              <th scope="col" className="px-6 py-3">
                Id unic
              </th>
              <th scope="col" className="px-6 py-3">
                Clădire
              </th>
              <th scope="col" className="px-6 py-3">
                Ore
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(rooms) ? (
              rooms.map((room) => (
                <tr
                  key={room.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(room.id)}
                    onEdit={() => handleEdit(room)}
                    showEdit={true}
                  />

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {room.name}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {room.unique_code}
                  </td>

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {room.building ? room.building.name : "-"}
                  </td>
                  <td scope="row" className="px-6 py-4">
                    <button
                      className={`${
                        room.sessions.length === 0
                          ? "text-gray-300 "
                          : "text-blue-400 underline hover:text-blue-500 transition-colors duration-300"
                      }`}
                      onClick={() =>
                        room.sessions.length > 0 &&
                        handleShowSessions(room.sessions)
                      }
                      disabled={room.sessions.length === 0}
                    >
                      Ore
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
                  Nu există săli
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {(isEditRoomModalOpen || isAddRoomModalOpen) && (
        <RoomForm
          isEditMode={isEditRoomModalOpen}
          room={isEditRoomModalOpen ? roomToEdit : null}
          buildings={buildings}
          sessions={sessions}
          onClose={() => {
            setIsEditRoomModalOpen(false);
            setIsAddRoomModalOpen(false);
          }}
          onSubmit={fetchRooms}
        />
      )}
      {isSessionsModalOpen && (
        <Modal
          items={selectedSessions}
          title="Ore"
          onClose={() => setIsSessionsModalOpen(false)}
          renderItem={(session) => {
            return (
              <>
                <div className="flex gap-2 justify-between text-center">
                  <div className="w-1/4 ">
                    {session.start.slice(0, 5)}-{session.end.slice(0, 5)}
                  </div>

                  <div className="w-1/4 ">
                    {sessionTypeMapping[session.type]}
                  </div>

                  <div className="w-1/4">Sem : {session.semester}</div>
                  <div className="w-1/4">
                    {weekTypeMapping[session.week_type]}
                  </div>
                  <div className="w-1/4">{dayMapping[session.day]}</div>
                </div>
              </>
            );
          }}
        />
      )}
      {showSuccessToast && (
        <SuccessToast
          message="Sala a fost ștearsă cu succes."
          onClose={() => setShowSuccessToast(false)}
        />
      )}

      {showErrorToast && (
        <ErrorToast
          message={errorMessage}
          onClose={() => setShowErrorToast(false)}
        />
      )}
    </>
  );
};

export default RoomTable;
