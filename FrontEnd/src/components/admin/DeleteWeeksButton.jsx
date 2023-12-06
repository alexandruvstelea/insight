import React from 'react';

export default function DeleteWeeksButton({ onDelete }) {
  return (

    <>
      <button
        type="button"
        className="deleteTableButton"
        onClick={onDelete} // Apelarea funcției onDelete
      >
        <h3>Sterge Saptamanile</h3>
      </button>
    </>
  )

}