'use client'

import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable, MRT_EditActionButtons } from 'material-react-table';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { Box, Button, IconButton, Tooltip, DialogTitle, DialogContent, DialogActions } from '@mui/material';


export default function Subjects({ professors, subjects, fetchSubjects }) {

  const addSubject = async (subject) => {
    const token = sessionStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('name', subject.name);
    formData.append('abbreviation', subject.abbreviation);
    formData.append('professor_id', subject.professor_id);
    formData.append('semester', subject.semester);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/subjects`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to add subject');
      }
      fetchSubjects();
    } catch (err) {
      console.error('Error adding subject:', err);
    }
  };

  const updateSubject = async (subject) => {
    const token = sessionStorage.getItem('access_token');

    const formData = new FormData();
    formData.append('new_name', subject.name);
    formData.append('new_abbreviation', subject.abbreviation);
    formData.append('new_professor_id', subject.professor_id);
    formData.append('new_semester', subject.semester);


    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/subjects/${subject.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update subject');
      }
      fetchSubjects();
    } catch (err) {
      console.error('Error updating subject:', err);
    }
  };

  const deleteSubject = async (id) => {
    const token = sessionStorage.getItem('access_token');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/subjects/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete subject');
      }
      fetchSubjects();
    } catch (err) {
      console.error('Error deleting subject:', err);
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
    { value: '1', label: '1' },
    { value: '2', label: '2' },
  ];

  const professorOptions = professors.map(professor => ({
    value: professor.id,
    label: `${professor.first_name} ${professor.last_name}`,
  }));

  const columns = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: 'ID Materie',
        size: 100,
        minSize: 30,
        enableEditing: false,
      },
      {
        accessorKey: 'name',
        header: 'Nume materie',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'abbreviation',
        header: 'Abreviere',
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'professor_id',
        header: 'Profesor',
        Cell: ({ cell }) => {
          const professor = professors.find(p => p.id === cell.getValue());
          return professor ? `${professor.first_name} ${professor.last_name}` : 'N/A';
        },
        editVariant: 'select',
        editSelectOptions: professorOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'semester',
        header: 'Semestru',
        editVariant: 'select',
        editSelectOptions: semesterOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
    ],
    [professors],
  );

  const table = useMaterialReactTable({
    columns,
    data: subjects || [],
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
        <DialogTitle variant="h3">Adauga Materie</DialogTitle>
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
    onEditingRowSave: handleSaveSubject,
    onCreatingRowSave: handleCreateSubject,
    renderTopToolbarCustomActions: ({ table }) => (
      <>
        <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true);
          }}
        >
          Adauga Materie
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
          <IconButton color="error" onClick={() => deleteSubject(row.original.id)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box >
    ),
  });

  return (
    <>
      <div className="table">
        <h1 className='tableTitle' >Tabel Materii</h1>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



