'use client'

import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable, MRT_EditActionButtons } from 'material-react-table';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { Box, Button, IconButton, Tooltip, DialogTitle, DialogContent, DialogActions } from '@mui/material';


export default function Courses({ courses, subjects, rooms, fetchCourses }) {

  const addCourse = async (course) => {
    const token = sessionStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('type', course.type);
    formData.append('subject_id', course.subject_id);
    formData.append('room_id', course.room_id);
    formData.append('day', course.day);
    formData.append('week_type', course.week_type);
    formData.append('start', course.start);
    formData.append('end', course.end);
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/courses`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to add courses');
      }
      fetchCourses();
    } catch (err) {
      console.error('Error adding courses:', err);
    }
  };

  const updateCourse = async (course) => {
    const token = sessionStorage.getItem('access_token');

    const formData = new FormData();
    formData.append('new_subject_id', course.subject_id);
    formData.append('new_type', course.type);
    formData.append('new_room_id', course.room_id);
    formData.append('new_day', course.day);
    formData.append('new_week_type', course.week_type);
    formData.append('new_start', course.start);
    formData.append('new_end', course.end);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/courses/${course.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update course');
      }
      fetchCourses();
    } catch (err) {
      console.error('Error updating course:', err);
    }
  };

  const deleteCourse = async (id) => {
    const token = sessionStorage.getItem('access_token');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/courses/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete course');
      }
      fetchCourses();
    } catch (err) {
      console.error('Error deleting course:', err);
    }
  };

  const handleSaveCourse = async ({ values, table }) => {
    await updateCourse(values);
    table.setEditingRow(null);
  };
  const handleCreateCourse = async ({ values, table }) => {
    await addCourse(values);
    table.setCreatingRow(null);
  };


  const typeOptions = [
    { value: '1', label: 'Curs' },
    { value: '2', label: 'Laborator' },
    { value: '3', label: 'Seminar' },
  ];
  const dayOptions = [
    { value: '0', label: 'Luni' },
    { value: '1', label: 'Marti' },
    { value: '2', label: 'Miercuri' },
    { value: '3', label: 'Joi' },
    { value: '4', label: 'Vineri' },
    { value: '5', label: 'Sambata' },
  ];
  const weekTypeOptions = [
    { value: '0', label: 'Ambele' },
    { value: '1', label: 'Impar' },
    { value: '2', label: 'Par' },
  ];

  const startEndOptions = [];
  for (let ora = 8; ora <= 22; ora += 2) {
    const oraFormatata = `${ora.toString().padStart(2, '0')}:00`;
    startEndOptions.push({ value: oraFormatata, label: oraFormatata });
  }

  const subjectOptions = subjects.map(subject => ({
    value: subject.id,
    label: `${subject.name}`,
  }));

  const roomOptions = rooms.map(room => ({
    value: room.id,
    label: `${room.name}`,
  }));

  const typeMap = typeOptions.reduce((acc, option) => {
    acc[option.value] = option.label;
    return acc;
  }, {});

  const dayMap = dayOptions.reduce((acc, option) => {
    acc[option.value] = option.label;
    return acc;
  }, {});

  const weekTypeMap = weekTypeOptions.reduce((acc, option) => {
    acc[option.value] = option.label;
    return acc;
  }, {});

  const columns = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: 'ID Curs',
        size: 100,
        minSize: 30,
        enableEditing: false,
      },
      {
        accessorKey: 'subject_id',
        header: 'Materie',
        Cell: ({ cell }) => {
          const subject = subjects.find(p => p.id === cell.getValue());
          return subject ? `${subject.name}` : 'N/A';
        },
        editVariant: 'select',
        editSelectOptions: subjectOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'type',
        header: 'Tipul',
        editVariant: 'select',
        editSelectOptions: typeOptions,
        Cell: ({ cell }) => typeMap[cell.getValue()] || 'N/A',
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'room_id',
        header: 'Sala de curs',
        Cell: ({ cell }) => {
          const room = rooms.find(p => p.id === cell.getValue());
          return room ? `${room.name}` : 'N/A';
        },
        editVariant: 'select',
        editSelectOptions: roomOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'day',
        header: 'Ziua saptamanii',
        editVariant: 'select',
        editSelectOptions: dayOptions,
        Cell: ({ cell }) => dayMap[cell.getValue()] || 'N/A',
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'week_type',
        header: 'Par/Impar',
        editVariant: 'select',
        editSelectOptions: weekTypeOptions,
        Cell: ({ cell }) => weekTypeMap[cell.getValue()] || 'N/A',
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'start',
        header: 'Ora de incepere',
        editVariant: 'select',
        editSelectOptions: startEndOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },
      {
        accessorKey: 'end',
        header: 'Ora de sfarsit',
        editVariant: 'select',
        editSelectOptions: startEndOptions,
        muiEditTextFieldProps: {
          select: true,
        },
        size: 120,
        minSize: 80,
        enableEditing: true,
      },

    ],
    [subjects, rooms],
  );

  const table = useMaterialReactTable({
    columns,
    data: courses || [],
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
        <DialogTitle variant="h3">Adauga Curs</DialogTitle>
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
    onEditingRowSave: handleSaveCourse,
    onCreatingRowSave: handleCreateCourse,
    renderTopToolbarCustomActions: ({ table }) => (
      <>
        <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true);
          }}
        >
          Adauga Curs
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
          <IconButton color="error" onClick={() => deleteCourse(row.original.id)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box >
    ),
  });

  return (
    <>
      <div className="table">
        <h1 className='tableTitle' >Tabel Cursuri</h1>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



