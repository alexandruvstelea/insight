"use client";
import { columnOption, defSelectColumnOption } from "./getTableConfig";
import React, { useMemo } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";

import { Delete as DeleteIcon } from "@mui/icons-material";
import { Box, IconButton, Tooltip, DialogTitle } from "@mui/material";

export default function Users({ users, fetchUsers, programmes }) {
  const deleteUser = async (id) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/users/${id}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to delete user");
      }
      fetchUsers();
    } catch (err) {
      console.error("Error deleting user:", err);
    }
  };

  const userType = [
    { value: "0", label: "Admin" },
    { value: "1", label: "User" },
  ];
  const userActive = [
    { value: "0", label: "Nu" },
    { value: "1", label: "Da" },
  ];

  const userTypeMap = userType.reduce((acc, option) => {
    acc[option.value] = option.label;
    return acc;
  }, {});

  const userActiveMap = userActive.reduce((acc, option) => {
    acc[option.value] = option.label;
    return acc;
  }, {});

  const programmeOptions = programmes.map((programme) => ({
    value: programme.id,
    label: `${programme.name}`,
  }));

  const columns = useMemo(
    () => [
      columnOption("id", "ID", 40, 40, false),
      columnOption("email", "Email", 100, 60, true),

      columnOption("programme_id", "Specializare", 200, 60, true, {
        ...defSelectColumnOption(programmeOptions),
        Cell: ({ cell }) => {
          const programme = programmes.find((p) => p.id === cell.getValue());
          return programme ? `${programme.name}` : "N/A";
        },
      }),
      columnOption("user_type", "User/Admin", 200, 60, true, {
        ...defSelectColumnOption(userType),
        Cell: ({ cell }) => userTypeMap[cell.getValue()] || "N/A",
      }),
      columnOption("active", "Cont Activat?", 200, 60, true, {
        ...defSelectColumnOption(userActive),
        Cell: ({ cell }) => userActiveMap[cell.getValue()] || "N/A",
      }),
    ],
    [programmes]
  );

  const table = useMaterialReactTable({
    columns,
    data: users || [],
    enablePagination: false,
    enableRowVirtualization: true,
    enableColumnActions: false,
    muiTableContainerProps: { sx: { maxHeight: "700px" } },
    initialState: {
      density: "comfortable",
      sorting: [
        {
          id: "id",
          desc: false,
        },
      ],
    },
    enableColumnPinning: true,
    displayColumnDefOptions: {
      "mrt-row-actions": {
        header: "Șterge",
        size: 50,
      },
    },
    positionActionsColumn: "first",
    editDisplayMode: "row",
    enableEditing: true,
    renderRowActions: ({ row }) => (
      <Box sx={{ display: "flex" }}>
        <Tooltip title="Șterge">
          <IconButton
            color="error"
            onClick={async () => {
              await deleteUser(row.original.id);
            }}
          >
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box>
    ),
  });

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: "center" }} variant="h3">
          Utilizatori
        </DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  );
}
