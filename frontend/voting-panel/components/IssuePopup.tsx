import { useState } from "react";

interface IssuePopupProps {
  onClose: () => void;
}

const IssuePopup: React.FC<IssuePopupProps> = ({ onClose }) => {
  const [bugDescription, setBugDescription] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("bugText", bugDescription);
    const text = formData.get("bugText")?.toString() || "";
    const timestamp = new Date().toISOString();
    console.log(timestamp);
    try {
      const response = await fetch(`${process.env.API_URL}/reports/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          timestamp,
        }),
      });

      if (response.status === 201) {
        onClose();
      } else if (response.status === 429) {
        setErrorMessage("Se poate trimite doar un raport pe zi.");
      } else {
        setErrorMessage("A apărut o eroare la trimiterea raportului.");
      }
    } catch (error) {
      setErrorMessage("Eroare.");
    }
  };

  return (
    <div
      id="popup-modal"
      className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-60 flex items-center justify-center z-50"
    >
      <div className="relative p-4 w-full max-w-md max-h-full">
        <div className="relative bg-white rounded-lg shadow">
          <form onSubmit={handleSubmit} className="px-4 py-6 text-center">
            <h3 className="mb-3 text-lg font-bold text-gray-700">
              Raportează o problemă
            </h3>
            <textarea
              className="w-full h-24 p-2 border border-gray-300 rounded-lg resize-none"
              placeholder="Descrie problema întâmpinată..."
              value={bugDescription}
              onChange={(e) => setBugDescription(e.target.value)}
              required
              minLength={10}
              maxLength={500}
            ></textarea>

            {errorMessage && (
              <p className="text-red-500 text-sm">{errorMessage}</p>
            )}
            <div className="flex gap-3 mt-4">
              <button
                type="button"
                onClick={onClose}
                className="bg-gray-200 w-full hover:bg-gray-300 text-gray-700 focus:ring-gray-400 text-base font-bold p-2 rounded transition-colors duration-300 whitespace-nowrap uppercase"
              >
                Anulează
              </button>
              <button
                type="submit"
                className="bg-blue-700 w-full hover:bg-blue-800 text-white text-base font-bold p-2 rounded transition-colors duration-300 whitespace-nowrap uppercase"
              >
                Trimite
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default IssuePopup;
