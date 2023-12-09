'use client'

import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable, MRT_EditActionButtons } from 'material-react-table';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { Box, Button, IconButton, Tooltip, DialogTitle, DialogContent, DialogActions } from '@mui/material';

export default function Professors({ professors, fetchProfessors }) {

  const addProfessor = async (professor) => {
    const token = sessionStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('first_name', professor.first_name);
    formData.append('last_name', professor.last_name);
    formData.append('title', professor.title);
    formData.append('gender', professor.gender);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/professors`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to add professor');
      }
      fetchProfessors();
    } catch (err) {
      console.error('Error adding professor:', err);
    }
  };

  const updateProfessor = async (professor) => {
    const token = sessionStorage.getItem('access_token');

    const formData = new FormData();
    formData.append('new_first_name', professor.first_name);
    formData.append('new_last_name', professor.last_name);
    formData.append('new_title', professor.title);
    formData.append('new_gender', professor.gender);


    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/professors/${professor.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update professor');
      }
      fetchProfessors();
    } catch (err) {
      console.error('Error updating professor:', err);
    }
  };

  const deleteProfessor = async (id) => {
    const token = sessionStorage.getItem('access_token');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/professors/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete professor');
      }
      fetchProfessors();
    } catch (err) {
      console.error('Error deleting professor:', err);
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
    { value: 'male', label: 'Masculin' },
    { value: 'female', label: 'Feminin' },
  ];


  const columns = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: 'ID Profesor',
        size: 100,
        minSize: 30,
        enableEditing: false,
      },
      {
        accessorKey: 'first_name',
        header: 'Nume',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'last_name',
        header: 'Prenume',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'title',
        header: 'Titlu',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'gender',
        header: 'Gen',
        Cell: ({ cell }) => cell.getValue() === 'female' ? 'Feminin' : (cell.getValue() === 'male' ? 'Masculin' : ''),
        editVariant: 'select',
        editSelectOptions: genderOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
    ],
    [],
  );

  const table = useMaterialReactTable({
    columns,
    data: professors || [],
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
        <DialogTitle variant="h3">Adauga Profesor</DialogTitle>
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
    onEditingRowSave: handleSaveProfessor,
    onCreatingRowSave: handleCreateProfessor,
    renderTopToolbarCustomActions: ({ table }) => (
      <>
        <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true);
          }}
        >
          Adauga Profesor
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
          <IconButton color="error" onClick={() => deleteProfessor(row.original.id)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box>
    ),
  });

  return (
    <>

      <div className="table">
        <h1 className='tableTitle' >Tabel Profesori</h1>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



