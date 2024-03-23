"use client";
import { tableConfig, columnOption } from "./getTableConfig";
import React, { useMemo } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
import { DialogTitle } from "@mui/material";

export default function Rooms({ rooms, fetchRooms }) {
  const addRoom = async (room) => {
    const formData = new FormData();
    formData.append("name", room.name);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms`, {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to add room");
      }
      fetchRooms();
    } catch (err) {
      console.error("Error adding room:", err);
    }
  };

  const updateRoom = async (room) => {
    const formData = new FormData();
    formData.append("new_room", room.name);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/rooms/${room.id}`,
        {
          method: "PUT",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update room");
      }
      fetchRooms();
    } catch (err) {
      console.error("Error updating room:", err);
    }
  };

  const handleSaveRoom = async ({ values, table }) => {
    await updateRoom(values);
    table.setEditingRow(null);
  };
  const handleCreateRoom = async ({ values, table }) => {
    await addRoom(values);
    table.setCreatingRow(null);
  };

  const columns = useMemo(
    () => [
      columnOption("id", "ID", 80, 40, false),
      columnOption("name", "Nume Sală", 200, 40, true),
    ],
    []
  );

  const table = useMaterialReactTable(
    tableConfig(
      columns,
      rooms,
      "sală de curs",
      handleCreateRoom,
      handleSaveRoom,
      "rooms",
      fetchRooms
    )
  );

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: "center" }} variant="h3">
          Tabel Săli de Curs
        </DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  );
}
