import React, { useState } from "react";
import { FormLabel, Input, FormControl, Stack, DialogContent, DialogTitle, ModalDialog, DialogActions, ModalClose, Modal, Textarea, Box, Button } from '@mui/joy';
import { FormControlLabel, Checkbox, ToggleButton, ToggleButtonGroup, TextField } from '@mui/material';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import ThumbDownAltIcon from '@mui/icons-material/ThumbDownAlt';
import ThumbDownOffAltIcon from '@mui/icons-material/ThumbDownOffAlt';
import { ToastContainer, toast } from 'react-toastify';

export default function Comments({ subjectId, fetchComments, fetchLikes }) {

  const [anonymous, setAnonymous] = React.useState(false);
  const [vote, setVote] = React.useState('');
  const [examGrade, setExamGrade] = React.useState('');
  const [comment, setComment] = React.useState('');
  const [openEmailModal, setOpenEmailModal] = React.useState(false);
  const [openCodeModal, setOpenCodeModal] = React.useState(false);
  const [emailForGenerate, setEmailForGenerate] = useState('');
  const [emailForCode, setEmailForCode] = useState('');
  const [code, setCode] = useState('');

  const handleVote = (event, newVote) => {
    if (newVote !== null) {
      setVote(newVote);
    }
  };

  const handleExamGradeChange = (event) => {
    setExamGrade(event.target.value);
  };

  const handleCommentChange = (event) => {
    setComment(event.target.value);
  };

  const handleAnonymousChange = (event) => {
    setAnonymous(event.target.checked);
  };

  const resetForm = () => {

    setEmailForCode('');
    setExamGrade('');
    setComment('');
    setVote('');
    setAnonymous(false);
    setCode('');
    setEmailForGenerate('');
  };

  const validateCommentBeforeOpeningModal = () => {
    if (comment.length < 30) {
      toast.error('Comentariul trebuie să conțină minim 30 de caractere.');
      return false;
    }

    if (comment.length > 700) {
      toast.error(`Comentariul NU poate contine mai mult de 700 de caractere.(${comment.length})`);
      return false;
    }

    if (!vote) {
      toast.error('Te rog selectează o opțiune (like sau dislike).');
      return false;
    }

    return true;
  };

  const validateEmailBeforeFetch = (email) => {
    const emailSuffix = "";

    if (email.includes(' ') || !email.endsWith(emailSuffix)) {
      toast.error('Email-ul nu este valid');
      return false;
    }
    return true;
  };

  const handleSubmitEmail = async () => {

    const formData = new FormData();
    formData.append('email', emailForGenerate);
    formData.append('subject_id', subjectId);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/comments`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorHtml = await response.text();
        const matches = /<p>(.*?)<\/p>/.exec(errorHtml);
        const errorMessage = matches && matches[1] ? matches[1] : 'A apărut o eroare';
        toast.error(errorMessage);
        throw new Error('Eroare la trimiterea datelor');
      }

      const data = await response.json();

      console.log(data);

      setOpenEmailModal(false);
      setOpenCodeModal(true)

    } catch (error) {
      console.error('A apărut o eroare:', error);
    }
  };
  const handleSubmitCode = async () => {
    const formData = new FormData();
    formData.append('email', emailForCode);
    formData.append('subject_id', subjectId);
    formData.append('new_comment', comment);
    formData.append('is_like', vote);
    formData.append('is_anonymous', anonymous);
    formData.append('code', code);

    const validGrades = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const grade = validGrades.includes(parseInt(examGrade)) ? examGrade : '-1';
    formData.append('new_grade', grade);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/comments`, {
        method: 'PUT',
        body: formData
      });

      if (!response.ok) {
        const errorHtml = await response.text();
        const matches = /<p>(.*?)<\/p>/.exec(errorHtml);
        const errorMessage = matches && matches[1] ? matches[1] : 'A apărut o eroare';
        toast.error(errorMessage);
        throw new Error('Eroare la trimiterea datelor');
      }

      const data = await response.json();
      fetchComments()
      fetchLikes()
      resetForm()
      setOpenCodeModal(false);
    } catch (error) {
      console.error('A apărut o eroare:', error);
    }
  };






  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable={false}
        pauseOnHover
        theme="colored"
      />

      <Textarea
        minRows={3}
        maxRows={4}
        name="comment"
        value={comment}
        onChange={handleCommentChange}
        size="md"
        placeholder="Comentariul tau..."
        variant="standard"
        sx={{
          border: '1px solid #bbb',
          backgroundColor: '#EFEFEF',
          '&:focus-within::before': { boxShadow: 'none' },
          width: '50rem',
        }}
        required
        startDecorator={
          <Box sx={{ display: 'flex', alignItems: 'center', flex: 1, borderBottom: '1px solid ', borderColor: 'divider' }}>
            <FormControlLabel
              control={<Checkbox onChange={handleAnonymousChange} />}
              label="Anonim"
              sx={{ '& .MuiSvgIcon-root': { fontSize: 20 }, my: -1 }} />
          </Box>
        }
        endDecorator={
          <Box
            sx={{
              display: 'flex',
              borderTop: '1px solid',
              borderColor: 'divider',
              flex: 'auto',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Box>
              <TextField
                type="number"
                id="examGrade"
                label="Notă examen"
                variant="standard"
                size="small"
                value={examGrade}
                onChange={handleExamGradeChange}
                sx={{ width: 120 }}
                inputProps={{
                  min: 1,
                  max: 9,
                }}
              />
            </Box>

            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
              }}>
              <ToggleButtonGroup
                value={vote}
                exclusive
                onChange={handleVote}
                aria-label="Voteaza profesorul"
              >
                <ToggleButton
                  value="0"
                  aria-label="like"
                  size="small"
                  sx={{
                    border: 'none',
                    '&.Mui-selected, &.Mui-selected:hover': {
                      backgroundColor: 'transparent'
                    }
                  }}>
                  {vote === '0' ? <ThumbUpAltIcon sx={{ color: '#0040C1' }} /> : <ThumbUpOffAltIcon sx={{ color: '#0040C1' }} />}
                </ToggleButton>
                <ToggleButton
                  value="1"
                  aria-label="dislike"
                  size="small"
                  sx={{
                    border: 'none',
                    color: '#0040C1',
                    '&.Mui-selected, &.Mui-selected:hover': {
                      backgroundColor: 'transparent'
                    }
                  }}>
                  {vote === '1' ? <ThumbDownAltIcon sx={{ color: '#0040C1' }} /> : <ThumbDownOffAltIcon sx={{ color: '#0040C1' }} />}
                </ToggleButton>
              </ToggleButtonGroup>

              <Button sx={{ ml: 1 }} onClick={() => {
                if (validateCommentBeforeOpeningModal()) {
                  setOpenEmailModal(true);
                }
              }}>Verifica</Button>
            </Box>
          </Box>
        }
      ></Textarea>
      <Modal open={openEmailModal} onClose={() => setOpenEmailModal(false)}>


        <ModalDialog sx={{ width: 400 }}>
          <ModalClose />
          <DialogTitle sx={{ textAlign: "center" }}>Verificare email institutional</DialogTitle>
          <DialogContent sx={{ fontSize: 14 }}>Pentru a putea lasa un comentariu este nevoie de verificarea email-ului institutional.</DialogContent>
          <form
            onSubmit={(event) => {
              event.preventDefault();
              if (validateEmailBeforeFetch(emailForGenerate)) {
                handleSubmitEmail()

              }

            }}
          >
            <Stack spacing={2}>
              <FormControl>
                <FormLabel>Email</FormLabel>
                <Input
                  value={emailForGenerate}
                  onChange={(e) => setEmailForGenerate(e.target.value)}
                  autoFocus
                  required
                />
              </FormControl>
              <DialogActions>
                <Button type="submit">
                  Genereaza cod
                </Button>
                <Button variant="soft" onClick={() => { setOpenEmailModal(false); setOpenCodeModal(true); }}>
                  Am deja codul
                </Button>
              </DialogActions>
            </Stack>
          </form>
        </ModalDialog >
      </Modal >

      <Modal open={openCodeModal} onClose={() => setOpenCodeModal(false)}>
        <ModalDialog sx={{ width: 400 }}>
          <ModalClose />
          <DialogTitle sx={{ textAlign: "center" }}>Verificare email institutional</DialogTitle>
          <DialogContent sx={{ fontSize: 14 }}>Introdu codul trimis pe email</DialogContent>
          <form
            onSubmit={(event) => {
              event.preventDefault();
              if (validateEmailBeforeFetch(emailForCode)) {
                handleSubmitCode()

              }
            }}
          >
            <Stack spacing={2}>
              <FormControl>
                <FormLabel>Email</FormLabel>
                <Input
                  value={emailForCode}
                  onChange={(e) => setEmailForCode(e.target.value)}
                  autoFocus
                  required
                />
              </FormControl>
              <FormControl>
                <FormLabel>Cod</FormLabel>
                <Input
                  type="number"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  autoFocus
                  required
                />
              </FormControl>
              <Button type="submit">Verifica cod</Button>
            </Stack>
          </form>
        </ModalDialog>
      </Modal >
    </>
  )
}