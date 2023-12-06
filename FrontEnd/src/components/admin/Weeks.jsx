'use client'

import React, { useMemo, useState, useEffect } from 'react';
import { MaterialReactTable, useMaterialReactTable } from 'material-react-table';
import DeleteWeeksButton from './DeleteWeeksButton';
import WeeksForm from './WeeksForm'

export default function Weeks() {

  const fetchWeeks = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weeks`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setWeeks(data)
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const deleteWeeks = async () => {
    const token = sessionStorage.getItem('access_token');
    const url = `${process.env.REACT_APP_API_URL}/weeks`;
    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });

      if (!response.ok) {
        throw new Error('Error deleting weeks');
      }
      setWeeks([]);
    }
    catch (err) {
      console.error('Fetch error:', err);
    }
  };


  const [weeks, setWeeks] = useState();

  useEffect(() => {

    fetchWeeks();
  }, []);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const columns = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: 'ID',
        size: 30,
      },
      {
        accessorKey: 'start',
        header: 'Start Date',
        size: 200,
        Cell: ({ cell }) => formatDate(cell.getValue()),
      },
      {
        accessorKey: 'end',
        header: 'End Date',
        size: 200,
        Cell: ({ cell }) => formatDate(cell.getValue()),
      },
      {
        accessorKey: 'semester',
        header: 'Semester',
        size: 100,
      },
    ],
    [],
  );


  const table = useMaterialReactTable({
    columns,
    data: weeks || [],
    enablePagination: false,
    enableRowVirtualization: true,
    muiTableContainerProps: { sx: { maxHeight: '700px' } },
    initialState: { density: 'compact' },

  });


  return (
    <>
      <div className="col-2-cont" >

        <WeeksForm updateWeeks={fetchWeeks} />

        <div id="weeksTable">
          <h1>Tabel Saptamani</h1>
          <DeleteWeeksButton onDelete={deleteWeeks} />
          <MaterialReactTable table={table} />;

        </div>
      </div>
    </>

  )
}
