import React, { useEffect, useState } from "react";
import { Box, Paper, Typography, Rating } from '@mui/material';
import Masonry from '@mui/lab/Masonry';


export default function DisplayComments({ comments }) {

  return (
    <>
      <Box sx={{ display: 'flex', justifyContent: 'center', margin: 'auto' }}>
        <Masonry columns={{ xs: 1, sm: 2, md: 3, lg: 3 }} spacing={4} >

          {comments.map((commentData) => (
            <Box key={commentData.id}
              sx={{
                width: 450,
                maxWidth: 450,
                wordBreak: 'break-word',
                fontFamily: 'Montserrat',
              }}
            >
              <Paper elevation={3} sx={{ p: 2, backgroundColor: 'rgba(255, 255, 255, 0.2)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    {commentData.email}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
                    {commentData.timestamp}
                  </Typography>
                </Box>
                <Typography variant="h6" component="div">
                  {commentData.comment}
                </Typography>
              </Paper>
            </Box>
          ))}
        </Masonry >
      </Box >
    </>
  )
}