import { ModalProps } from "@/utils/interfaces";

const Modal = <T,>({
  items,
  title,
  onClose,
  renderItem,
  isTable,
}: ModalProps<T>) => {
  return (
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex flex-col gap-5">
          <h3 className="text-xl font-semibold text-center text-white">
            {title}
          </h3>

          {isTable ? (
            <table className="table-auto w-full text-left text-gray-300">
              <thead>
                <tr>
                  <th>Interval</th>
                  <th>Zi</th>
                  <th>Tip</th>
                  <th>Semestru</th>
                  <th>Tip Săptămână</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={index}>{renderItem(item)}</tr>
                ))}
              </tbody>
            </table>
          ) : (
            <ul className="list-disc pl-4">
              {items.map((item, index) => (
                <li className="text-gray-300 text-base" key={index}>
                  {renderItem(item)}
                </li>
              ))}
            </ul>
          )}

          <button className="button" onClick={onClose}>
            Închide
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
