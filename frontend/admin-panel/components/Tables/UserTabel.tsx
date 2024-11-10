"use client";

import { useState, FC } from "react";
import { UserTableProps } from "@/utils/interfaces";
import HeaderSection from "@/components/HeaderSection";
import TableActions from "@/components/TableActions";
import SuccessToast from "@/components/SuccessToast";
import ErrorToast from "@/components/ErrorToast";

const UserTable: FC<UserTableProps> = ({ users = [], fetchUsers }) => {
  const [showSuccessToast, setShowSuccessToast] = useState(false);
  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți acest user?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/users/${id}`, {
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
        fetchUsers();
      } catch (error: any) {
        setErrorMessage(error.message);
        setShowErrorToast(true);
      }
    }
  };

  return (
    <>
      <div className=" p-4 flex flex-col items-center justify-center glass-background ">
        <HeaderSection title="Useri" count={users?.length || 0} buttons={[]} />
        <table className="w-full text-base text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Acțiuni
              </th>
              <th scope="col" className="px-6 py-3">
                Email
              </th>
              <th scope="col" className="px-6 py-3">
                Rol
              </th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(users) ? (
              users.map((user) => (
                <tr
                  key={user.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <TableActions
                    onDelete={() => handleDelete(user.id)}
                    showEdit={false}
                  />
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {user.email}
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium   text-white"
                  >
                    {user.role}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={8}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există users
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {showSuccessToast && (
        <SuccessToast
          message="User-ul a fost ștearsă cu succes."
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

export default UserTable;
