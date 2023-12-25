'use client'
import { columnOption } from './getTableConfig'
import React, { useMemo } from 'react';
import { MaterialReactTable, useMaterialReactTable } from 'material-react-table';
import {
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { Box, IconButton, Tooltip, DialogTitle } from '@mui/material';

export default function Comments({ comments, fetchCommnets }) {

  const deleteComment = async (id) => {
    const token = sessionStorage.getItem('access_token');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/comments/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete comment');
      }
      fetchCommnets();
    } catch (err) {
      console.error('Error deleting comment:', err);
    }
  };

  const columns = useMemo(
    () => [
      columnOption('id', 'ID', 40, 40, false),
      columnOption('sentiment', 'Procentaj', 100, 60, true),

      columnOption('comment', 'Comentariu', 900, 800, true),
    ],
    [],
  );

  const table = useMaterialReactTable({
    columns,
    data: comments || [],
    enablePagination: false,
    enableRowVirtualization: true,
    enableColumnActions: false,
    muiTableContainerProps: { sx: { maxHeight: '700px' } },
    initialState: {
      density: 'comfortable',
      sorting: [{
        id: 'id',
        desc: false
      }],
    },
    enableColumnPinning: true,
    displayColumnDefOptions: {
      'mrt-row-actions': {
        header: 'Șterge',
        size: 50,
      },
    },
    positionActionsColumn: 'first',
    editDisplayMode: 'row',
    enableEditing: true,
    renderRowActions: ({ row }) => (
      <Box sx={{ display: 'flex' }}>
        <Tooltip title="Șterge">
          <IconButton color="error" onClick={async () => {
            await deleteComment(row.original.id);
          }}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box >
    ),
  });


  return (
    <>
      <div className="table">
        <DialogTitle sx={{ textAlign: 'center' }} variant="h3">Comentarii</DialogTitle>
        <MaterialReactTable table={table} />
      </div>
    </>
  )
}



