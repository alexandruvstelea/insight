import { TableActionsProps } from "@/utils/interfaces";
import React from "react";

const TableActions: React.FC<TableActionsProps> = ({
  onDelete,
  onEdit,
  showEdit = true,
}) => {
  return (
    <td scope="row" className="w-[100px] px-6 py-4">
      <div className="flex justify-between">
        {showEdit && (
          <button onClick={onEdit}>
            <img
              src="/svgs/edit.svg"
              className="w-auto h-6 hover:brightness-75 transition duration-300"
              alt="Edit"
            />
          </button>
        )}
        <button onClick={onDelete}>
          <img
            src="/svgs/delete.svg"
            className="w-auto h-6 hover:brightness-75 transition duration-300"
            alt="Delete"
          />
        </button>
      </div>
    </td>
  );
};

export default TableActions;
