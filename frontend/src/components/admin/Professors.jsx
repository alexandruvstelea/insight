"use client";
import {
  tableConfig,
  columnOption,
  defSelectColumnOption,
} from "./getTableConfig";
import React, { useMemo } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
import { DialogTitle } from "@mui/material";

export default function Professors({ professors, fetchProfessors }) {
  const addProfessor = async (professor) => {
    const formData = new FormData();
    formData.append("first_name", professor.first_name);
    formData.append("last_name", professor.last_name);
    formData.append("title", professor.title);
    formData.append("gender", professor.gender);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/professors`,
        {
          method: "POST",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to add professor");
      }
      fetchProfessors();
    } catch (err) {
      console.error("Error adding professor:", err);
    }
  };

  const updateProfessor = async (professor) => {
    const formData = new FormData();
    formData.append("new_first_name", professor.first_name);
    formData.append("new_last_name", professor.last_name);
    formData.append("new_title", professor.title);
    formData.append("new_gender", professor.gender);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/professors/${professor.id}`,
        {
          method: "PUT",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update professor");
      }
      fetchProfessors();
    } catch (err) {
      console.error("Error updating professor:", err);
    }
  };

  const handleSaveProfessor = async ({ values, table }) => {
    await updateProfessor(values);
    table.setEditingRow(null);
  };
  const handleCreateProfessor = async ({ values, table }) => {
    await addProfessor(values);
    table.setCreatingRow(null);
  };

  const genderOptions = [
    { value: "male", label: "Masculin" },
    { value: "female", label: "Feminin" },
  ];

  const columns = useMemo(
    () => [
      columnOption("id", "ID", 100, 30, false),
      columnOption("last_name", "Nume", 120, 80, true),
      columnOption("first_name", "Prenume", 120, 80, true),
      columnOption("gender", "Gen", 120, 80, true, {
        ...defSelectColumnOption(genderOptions),
        Cell: ({ cell }) =>
          cell.getValue() === "female"
            ? "Feminin"
            : cell.getValue() === "male"
            ? "Masculin"
            : "",
      }),
    ],
    []
  );

  const table = useMaterialReactTable(
    tableConfig(
      columns,
      professors,
      "profesor",
      handleCreateProfessor,
      handleSaveProfessor,
      "professors",
      fetchProfessors
    )
  );

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: "center" }} variant="h3">
          Tabel Profesori
        </DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  );
}
