'use client'

import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable, MRT_EditActionButtons } from 'material-react-table';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { Box, Button, IconButton, Tooltip, DialogTitle, DialogContent, DialogActions } from '@mui/material';


export default function Rooms({ rooms, fetchRooms }) {
  const addRoom = async (room) => {
    const token = sessionStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('name', room.name);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to add room');
      }
      fetchRooms();
    } catch (err) {
      console.error('Error adding room:', err);
    }
  };

  const updateRoom = async (room) => {
    const token = sessionStorage.getItem('access_token');

    const formData = new FormData();
    formData.append('new_room', room.name);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms/${room.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update room');
      }
      fetchRooms();
    } catch (err) {
      console.error('Error updating room:', err);
    }
  };

  const deleteRoom = async (id) => {
    const token = sessionStorage.getItem('access_token');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/rooms/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete room');
      }
      fetchRooms();
    } catch (err) {
      console.error('Error deleting rooms:', err);
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
      {
        accessorKey: 'id',
        header: 'ID Sala',
        size: 100,
        minSize: 30,
        enableEditing: false,
      },
      {
        accessorKey: 'name',
        header: 'Nume Sala',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
    ],
    [],
  );

  const table = useMaterialReactTable({
    columns,
    data: rooms || [],
    createDisplayMode: 'modal',
    editDisplayMode: 'row',
    enableEditing: true,
    enablePagination: false,
    enableRowVirtualization: true,
    positionActionsColumn: 'last',

    displayColumnDefOptions: {
      'mrt-row-actions': {
        header: 'Edit/Delete',
        size: 100,
        minSize: 80,
      },
    },
    muiTableContainerProps: { sx: { maxHeight: '700px' } },
    initialState: {
      density: 'compact',
      sorting: [{
        id: 'id',
        desc: false
      }],
    },

    renderCreateRowDialogContent: ({ table, row, internalEditComponents }) => (
      <>
        <DialogTitle variant="h3">Adauga Sala de curs</DialogTitle>
        <DialogContent
          sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
        >
          {internalEditComponents.filter(component => component.key !== 'mrt-row-create_id')}

        </DialogContent>
        <DialogActions>
          <MRT_EditActionButtons variant="text" table={table} row={row} />
        </DialogActions>
      </>
    ),
    onEditingRowSave: handleSaveRoom,
    onCreatingRowSave: handleCreateRoom,
    renderTopToolbarCustomActions: ({ table }) => (
      <>
        <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true);
          }}
        >
          Adauga Sala de Curs
        </Button>
      </>
    ),
    renderRowActions: ({ row, table }) => (
      <Box sx={{ display: 'flex', gap: '1rem' }}>
        <Tooltip title="Edit">
          <IconButton onClick={() => table.setEditingRow(row)}>
            <EditIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title="Delete">
          <IconButton color="error" onClick={() => deleteRoom(row.original.id)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box >
    ),
  });

  return (
    <>
      <div className="table">
        <h1 className='tableTitle' >Tabel Sali de Curs</h1>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



