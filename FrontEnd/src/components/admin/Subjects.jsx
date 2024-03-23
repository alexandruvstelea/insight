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

export default function Subjects({ professors, subjects, fetchSubjects }) {
  const addSubject = async (subject) => {
    const formData = new FormData();
    formData.append("name", subject.name);
    formData.append("abbreviation", subject.abbreviation);
    formData.append("professor_id", subject.professor_id);
    formData.append("semester", subject.semester);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/subjects`,
        {
          method: "POST",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to add subject");
      }
      fetchSubjects();
    } catch (err) {
      console.error("Error adding subject:", err);
    }
  };

  const updateSubject = async (subject) => {
    const formData = new FormData();
    formData.append("new_name", subject.name);
    formData.append("new_abbreviation", subject.abbreviation);
    formData.append("new_professor_id", subject.professor_id);
    formData.append("new_semester", subject.semester);

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/subjects/${subject.id}`,
        {
          method: "PUT",
          credentials: "include",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update subject");
      }
      fetchSubjects();
    } catch (err) {
      console.error("Error updating subject:", err);
    }
  };

  const handleSaveSubject = async ({ values, table }) => {
    await updateSubject(values);
    table.setEditingRow(null);
  };
  const handleCreateSubject = async ({ values, table }) => {
    await addSubject(values);
    table.setCreatingRow(null);
  };

  const semesterOptions = [
    { value: "1", label: "1" },
    { value: "2", label: "2" },
  ];

  const professorOptions = professors.map((professor) => ({
    value: professor.id,
    label: `${professor.first_name} ${professor.last_name}`,
  }));

  const columns = useMemo(
    () => [
      columnOption("id", "ID", 80, 40, false),
      columnOption("name", "Nume materie", 120, 80, true),
      columnOption("abbreviation", "Abreviere", 120, 80, true),
      columnOption("professor_id", "Profesor", 120, 80, true, {
        ...defSelectColumnOption(professorOptions),
        Cell: ({ cell }) => {
          const professor = professors.find((p) => p.id === cell.getValue());
          return professor
            ? `${professor.first_name} ${professor.last_name}`
            : "N/A";
        },
      }),
      columnOption("semester", "Semestru", 120, 80, true, {
        ...defSelectColumnOption(semesterOptions),
      }),
    ],
    [professors]
  );

  const table = useMaterialReactTable(
    tableConfig(
      columns,
      subjects,
      "materie",
      handleCreateSubject,
      handleSaveSubject,
      "subjects",
      fetchSubjects
    )
  );

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: "center" }} variant="h3">
          Tabel Materii
        </DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  );
}
