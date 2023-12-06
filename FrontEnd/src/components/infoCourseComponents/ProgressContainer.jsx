import LinearProgress from '@mui/material/LinearProgress';
import React, { useState, useEffect } from 'react';

export default function ProgressContainer({ name, percentage }) {
  const MIN = 0;
  const MAX = 100;

  const calculatePercentage = (value) => ((value - MIN) * 100) / (MAX - MIN);
  return (
    <>
      <div className="progress-container">
        <span className="text-m">{name}</span>
        <div className="progress-bar">
          <LinearProgress style={{ height: '7px' }} variant="determinate" value={calculatePercentage(percentage)} />
        </div>
        <span className="text-m">{percentage}%</span>
      </div>
    </>
  )
}