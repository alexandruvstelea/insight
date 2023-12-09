import React from 'react';

export default function DeleteWeeksButton({ onDelete }) {
  return (

    <>
      <button
        type="button"
        onClick={onDelete}
      >
        <h3>Sterge Saptamanile</h3>
      </button>
    </>
  )

}