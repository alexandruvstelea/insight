import Link from "next/link";

interface SuccessPopupProps {
  redirectCountdown: number;
}

const SuccessPopup: React.FC<SuccessPopupProps> = ({ redirectCountdown }) => {
  return (
    <div
      id="popup-modal"
      className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-60 flex items-center justify-center z-50"
    >
      <div className="relative p-4 w-full max-w-md max-h-full">
        <div className="relative bg-white rounded-lg shadow">
          <div className="px-2 py-4 md:p-5 text-center">
            <img
              src="/svgs/ok.svg"
              className="mx-auto mb-4 w-12 h-auto"
              alt="Succes"
            />
            <h3 className="mb-5 text-lg font-normal text-gray-700">
              Evaluarea a fost trimisă cu succes!
            </h3>
            <Link
              href="https://www.insightbv.ro"
              className="text-white bg-blue-600 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
            >
              Vei fi redirecționat în {redirectCountdown} secunde.
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SuccessPopup;
