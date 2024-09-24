import { ButtonGroupProps } from "@/utils/interfaces";
import React from "react";

const ButtonGroup: React.FC<ButtonGroupProps> = ({ onClose, isEditMode }) => {
  return (
    <div className="flex justify-between mt-6">
      <button
        type="button"
        onClick={onClose}
        className="button bg-gray-500 hover:bg-gray-600"
      >
        Închide
      </button>
      <button type="submit" className="button">
        {isEditMode ? "Editează" : "Adaugă"}
      </button>
    </div>
  );
};

export default ButtonGroup;
