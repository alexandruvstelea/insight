import React from "react";
import { Box, Paper, Typography } from '@mui/material';
import Masonry from '@mui/lab/Masonry';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export default function DisplayComments({ comments }) {

  const theme = createTheme({
    breakpoints: {
      values: {
        xs: 450,
        sm: 800,
        md: 900,
        lg: 1200,
        xl: 1536,
      },
    },
  });

  return (
    <>
      <ThemeProvider theme={theme}>
        <Box sx={{ display: 'flex', justifyContent: 'center', margin: 'auto', width: "90vw", mt: 10 }}>
          <Masonry columns={{ xs: 1, sm: 1, md: 2, lg: 3 }} spacing={4} >

            {comments.map((commentData) => (
              <Box key={commentData.id}
                sx={{

                  width: 500,
                  wordBreak: 'break-word',
                  fontFamily: 'Montserrat',
                  [theme.breakpoints.down('md')]: {
                    width: '350px',
                    maxWidth: '95%',
                    minWidth: '95%',
                  },
                  [theme.breakpoints.down('xs')]: {
                    width: '350px',
                    maxWidth: '90%',
                    minWidth: '90%',
                  },
                }}
              >
                <Paper elevation={3} sx={{ p: 2, backgroundColor: 'rgba(255, 255, 255, 0.2)', boxShadow: '1px 2px 6px  rgba(3, 138, 255,0.5)' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="body2" color="#0040C1" >
                      {commentData.email}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
                      {commentData.timestamp}
                    </Typography>
                  </Box>
                  <Typography variant="h6" component="div" sx={{ fontSize: 17 }}>
                    {commentData.comment}
                  </Typography>
                </Paper>
              </Box>
            ))}
          </Masonry >
        </Box >
      </ThemeProvider>
    </>
  )
}