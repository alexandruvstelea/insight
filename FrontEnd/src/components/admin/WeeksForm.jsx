import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { FormLabel } from '@mui/material';

export default function WeeksForm({ updateWeeks }) {

  const handleSubmit = async (event) => {
    const token = sessionStorage.getItem('access_token');
    event.preventDefault();

    const formData = new FormData(event.target);
    console.log(formData.getAll('intervals'))

    const url = `${process.env.REACT_APP_API_URL}/weeks`;
    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const result = await response.json();
      console.log(result);
      updateWeeks()
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };
  return (
    <>

      <div className="form-container">
        <h1>Generare Saptamani</h1>
        <form autoComplete="off" onSubmit={handleSubmit}>

          <FormLabel>Prima zi din anul universitar:</FormLabel>
          <TextField
            type="date"
            name='year_start'
            required
            fullWidth
            variant='outlined'
            size='small'
          />

          <FormLabel>Activitate didactica:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="12"
            size='small'
          />
          <FormLabel>Vacanta:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="2"
            size='small'
          />
          <FormLabel>Activitate didactica:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="2"
            size='small'
          />
          <FormLabel>Sesiune:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="3"
            size='small'
          />
          <FormLabel>Vacanta:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="1"
            size='small'
          />
          <FormLabel>Activitate didactica:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="10"
            size='small'
          />
          <FormLabel>Vacanta:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="1"
            size='small'
          />
          <FormLabel>Activitate didactica:</FormLabel>
          <TextField
            type="number"
            name='intervals'
            required
            fullWidth
            variant='outlined'
            defaultValue="4"
            size='small'
          />
          <Button variant="outlined" type="submit">Generare</Button>
        </form>
      </div>
    </>
  );
};


