import React from "react";

interface ModalProps<T> {
  items: T[];
  title: string;
  onClose: () => void;
  renderItem: (item: T) => React.ReactNode;
}

const ModalSession = <T,>({
  items,
  title,
  onClose,
  renderItem,
}: ModalProps<T>) => {
  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded  max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex flex-col gap-5">
          <h3 className="text-xl font-semibold text-center text-white">
            {title}
          </h3>
          <ul className="list-disc pl-4">
            {items.map((item, index) => (
              <li className="text-gray-300 text-base" key={index}>
                {renderItem(item)}
              </li>
            ))}
          </ul>
          <button className="button" onClick={onClose}>
            Închide
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModalSession;
