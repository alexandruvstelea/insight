"use client";

import { useState, FC } from "react";
import { UserTableProps } from "@/utils/interfaces";
import HeaderSection from "@/components/HeaderSection";
import TableActions from "@/components/TableActions";
import { useNotification } from "@/context/NotificationContext";

const UserTable: FC<UserTableProps> = ({ users = [], fetchUsers }) => {
  const { notify } = useNotification();

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

        notify("User-ul a fost sters cu succes.", "success");
        fetchUsers();
      } catch (error: any) {
        notify(error.message, "error");
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
    </>
  );
};

export default UserTable;
