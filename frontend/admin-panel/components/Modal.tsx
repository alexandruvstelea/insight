// components/Modal.tsx

import React from "react";

interface ModalProps<T> {
  items: T[];
  title: string;
  onClose: () => void;
  renderItem: (item: T) => React.ReactNode; // Function to render each item
}

const Modal = <T,>({ items, title, onClose, renderItem }: ModalProps<T>) => {
  return (
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <ul className="list-disc pl-4">
          {items.map((item, index) => (
            <li key={index}>{renderItem(item)}</li>
          ))}
        </ul>
        <button
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
          onClick={onClose}
        >
          Închide
        </button>
      </div>
    </div>
  );
};

export default Modal;
