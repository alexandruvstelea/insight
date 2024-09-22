"use client";

import DeleteSVG from "@/components/svgs/DeleteSVG";
import EditSVG from "@/components/svgs/EditSVG";
import SessionForm from "@/components/Sessions/SessionForm";
import { useState, FC } from "react";
import { Session } from "@/utils/types";
import { SessionTableProps } from "@/utils/interfaces";
import {
  weekTypeMapping,
  dayMapping,
  sessionTypeMapping,
} from "@/utils/functions";
import HeaderSection from "../HeaderSection";

const SessionTable: FC<SessionTableProps> = ({
  sessions = [],
  rooms,
  faculties,

  fetchSessions,
}) => {
  const [isAddSessionModalOpen, setIsAddSessionModalOpen] = useState(false);

  const [isEditSessionModalOpen, setIsEditSessionModalOpen] = useState(false);
  const [sessionToEdit, setSessionToEdit] = useState<Session | null>(null);

  const handleEdit = (session: Session) => {
    setSessionToEdit(session);
    setIsEditSessionModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți această sesiune?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/sessions/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("An error occurred while deleting the session");
        }

        fetchSessions();
      } catch (error) {
        alert("A apărut o eroare la ștergerea orei");
      }
    }
  };

  return (
    <>
      <div className="p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="ORE"
          buttons={[
            {
              text: "ADAUGĂ ORĂ",
              onClick: () => setIsAddSessionModalOpen(true),
            },
          ]}
          count={sessions?.length || 0}
        />
        <table className="w-full text-md text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Curs
              </th>
              <th scope="col" className="px-6 py-3">
                Tip
              </th>
              <th scope="col" className="px-6 py-3">
                Semestru
              </th>
              <th scope="col" className="px-6 py-3">
                Tipul săptămânii
              </th>
              <th scope="col" className="px-6 py-3">
                Ora start
              </th>
              <th scope="col" className="px-6 py-3">
                Ora sfârșit
              </th>
              <th scope="col" className="px-6 py-3">
                Zi
              </th>
              <th scope="col" className="px-6 py-3">
                Sală
              </th>

              <th scope="col" className="px-6 py-3">
                Facultate
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(sessions) ? (
              sessions.map((session) => (
                <tr
                  key={session.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <td scope="row" className="[100px] px-6 py-4">
                    <div className="flex justify-around">
                      <button onClick={() => handleEdit(session)}>
                        <EditSVG />
                      </button>
                      <button onClick={() => handleDelete(session.id)}>
                        <DeleteSVG />
                      </button>
                    </div>
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {session.subject
                      ? `${session.subject.name} (${session.subject.abbreviation})`
                      : ""}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {sessionTypeMapping[session.type]}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {session.semester}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {weekTypeMapping[session.week_type]}
                  </td>

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {session.start.slice(0, 5)}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {session.end.slice(0, 5)}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {dayMapping[session.day]}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {session.room ? session.room.name : ""}
                  </td>

                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {Array.isArray(faculties) &&
                    Array.isArray(session.faculty_id) &&
                    session.faculty_id.length > 0
                      ? faculties.find(
                          (faculty) => faculty.id === session.faculty_id[0]
                        )?.abbreviation || "-"
                      : "-"}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={10}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există ore
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {(isEditSessionModalOpen || isAddSessionModalOpen) && (
        <SessionForm
          isEditMode={isEditSessionModalOpen}
          session={isEditSessionModalOpen ? sessionToEdit : null}
          rooms={rooms}
          faculties={faculties}
          onClose={() => {
            setIsEditSessionModalOpen(false);
            setIsAddSessionModalOpen(false);
          }}
          onSubmit={fetchSessions}
        />
      )}
    </>
  );
};

export default SessionTable;
