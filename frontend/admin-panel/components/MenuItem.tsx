import { MenuItemProps } from "@/utils/interfaces";
import React from "react";

const MenuItem: React.FC<MenuItemProps> = ({ label, isActive, onClick }) => {
  return (
    <li>
      <button
        onClick={onClick}
        className={`menuButton ${
          isActive ? "bg-gray-600 text-white" : "text-white"
        }`}
      >
        {label}
      </button>
    </li>
  );
};

export default MenuItem;
