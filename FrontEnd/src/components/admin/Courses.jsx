'use client'
import { tableConfig, columnOption, defSelectColumnOption } from './getTableConfig'
import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable } from 'material-react-table';
import { DialogTitle } from '@mui/material';
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
      columnOption('id', 'ID', 80, 40, false),
      columnOption('subject_id', 'Materie', 120, 80, true,
        {
          ...defSelectColumnOption(subjectOptions),
          Cell: ({ cell }) => {
            const subject = subjects.find(p => p.id === cell.getValue());
            return subject ? `${subject.name}` : 'N/A';
          },
        }),
      columnOption('type', 'Tipul', 120, 80, true,
        {
          ...defSelectColumnOption(typeOptions),
          Cell: ({ cell }) => typeMap[cell.getValue()] || 'N/A',
        }),
      columnOption('room_id', 'Sală de curs', 120, 80, true,
        {
          ...defSelectColumnOption(roomOptions),
          Cell: ({ cell }) => {
            const room = rooms.find(p => p.id === cell.getValue());
            return room ? `${room.name}` : 'N/A';
          },
        }),
      columnOption('day', 'Ziua săptămânii', 120, 80, true,
        {
          ...defSelectColumnOption(dayOptions),
          Cell: ({ cell }) => dayMap[cell.getValue()] || 'N/A',
        }),
      columnOption('week_type', 'Par/Impar', 120, 80, true,
        {
          ...defSelectColumnOption(weekTypeOptions),
          Cell: ({ cell }) => weekTypeMap[cell.getValue()] || 'N/A',
        }),
      columnOption('start', 'Ora de incepere', 120, 80, true,
        {
          ...defSelectColumnOption(startEndOptions),
        }),
      columnOption('end', 'Ora de sfarșit', 120, 80, true,
        {
          ...defSelectColumnOption(startEndOptions),
        }),
    ],
    [subjects, rooms],
  );
  const table = useMaterialReactTable(tableConfig(columns, courses, 'curs', handleCreateCourse, handleSaveCourse, 'courses', fetchCourses));

  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: 'center' }} variant="h3">Tabel Cursuri</DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



