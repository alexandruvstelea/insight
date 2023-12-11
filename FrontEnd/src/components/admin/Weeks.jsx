'use client'
import { tableConfigDef, columnOption } from './getTableConfig'
import React, { useMemo, useState } from 'react';
import { MaterialReactTable, useMaterialReactTable } from 'material-react-table';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import TextField from '@mui/material/TextField';

export default function Weeks({ weeks, fetchWeeks }) {
  const [open, setOpen] = useState(false);

  const addWeeks = async (weeks) => {
    weeks.preventDefault()
    const token = sessionStorage.getItem('access_token');
    const formData = new FormData(weeks.target);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weeks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to add weeks');
      }
      fetchWeeks();
      handleClose();
    } catch (err) {
      console.error('Error adding weeks:', err);
    }
  };

  const deleteWeeks = async () => {
    const token = sessionStorage.getItem('access_token');

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/weeks`, {
        method: "DELETE",
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete weeks');
      }
      fetchWeeks();
    }
    catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const openDeleteConfirmModal = () => {
    if (window.confirm('Ești sigur ca vrei sa stergi săptămânile?')) {
      deleteWeeks();
    }
  };

  const columns = useMemo(
    () => [
      columnOption('id', 'ID', 80, 40, false),
      columnOption('start', 'Început', 220, 100, false, {
        Cell: ({ cell }) => formatDate(cell.getValue()),
      }),
      columnOption('end', 'Sfarșit', 220, 100, false, {
        Cell: ({ cell }) => formatDate(cell.getValue()),
      }),
      columnOption('semester', 'Semestru', 170, 100, false),
    ],
    [],
  );


  const table = useMaterialReactTable({
    ...tableConfigDef(columns, weeks),
    renderTopToolbarCustomActions: () => (
      <>
        <Box sx={{ display: 'flex', gap: '1rem' }}>
          <Button
            variant="contained"
            onClick={handleClickOpen}
          >
            Adaugă Săptămânile
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={() => openDeleteConfirmModal()}
          >

            Sterge Săptămânile
          </Button>
        </Box>
      </>
    ),
  });


  return (
    <>
      <Dialog
        open={open}
        onClose={handleClose}
        sx={{
          '& .MuiDialog-paper': { width: '444px' }
        }}
      >
        <form onSubmit={addWeeks} >
          <DialogTitle variant="h4">Adaugă Săptămâni</DialogTitle>
          <DialogContent
            sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
          >
            <TextField
              type='date'
              label="Prima zi din anul universitar"
              name="year_start"
              variant='standard'
              required
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              type="number"
              label='Activitate didactică'
              name='intervals'
              variant='standard'
              required
            />
            <TextField
              type="number"
              label='Vacanță'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Activitate didactică'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Sesiune'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Vacantă'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Activitate didactică'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Vacanță'
              name='intervals'
              variant='standard'
              required

            />
            <TextField
              type="number"
              label='Activitate didactică'
              name='intervals'
              variant='standard'
              required

            />
          </DialogContent>
          <DialogActions >
            <Button onClick={handleClose}>Cancel</Button>
            <Button type='submit' variant='contained' color='primary'>Save</Button>
          </DialogActions>
        </form>
      </Dialog>
      <div className='table'>
        <div>
          <DialogTitle sx={{ textAlign: 'center' }} variant="h3">Tabel Săptămâni</DialogTitle>
          <MaterialReactTable table={table} />
        </div>
      </div>
    </>

  )
}
