"use client";
import { tableConfig, columnOption } from "./getTableConfig";
import React, { useMemo } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
import { DialogTitle } from "@mui/material";

export default function Programmes({ programmes, fetchProgrammes }) {
  const addProgramme = async (programme) => {
    const formData = new FormData();
    formData.append("name", programme.name);
    formData.append("abbreviation", programme.abbreviation);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/programmes`,
        {
          method: "POST",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to add programme");
      }
      fetchProgrammes();
    } catch (err) {
      console.error("Error adding programme:", err);
    }
  };

  const updateProgramme = async (programme) => {
    const formData = new FormData();
    formData.append("new_name", programme.name);
    formData.append("new_abbreviation", programme.name);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/programmes/${programme.id}`,
        {
          method: "PUT",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update programme");
      }
      fetchProgrammes();
    } catch (err) {
      console.error("Error updating programme:", err);
    }
  };

  const handleSaveProgramme = async ({ values, table }) => {
    await updateProgramme(values);
    table.setEditingRow(null);
  };
  const handleCreateProgramme = async ({ values, table }) => {
    await addProgramme(values);
    table.setCreatingRow(null);
  };

  const columns = useMemo(
    () => [
      columnOption("id", "ID", 80, 40, false),
      columnOption("name", "Nume specializare", 200, 40, true),
      columnOption("abbreviation", "Abreviere", 200, 40, true),
    ],
    []
  );

  const table = useMaterialReactTable(
    tableConfig(
      columns,
      programmes,
      "specializare",
      handleCreateProgramme,
      handleSaveProgramme,
      "programmes",
      fetchProgrammes
    )
  );

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: "center" }} variant="h3">
          Tabel Specializări
        </DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  );
}
