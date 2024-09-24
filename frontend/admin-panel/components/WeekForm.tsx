import React, { useState } from "react";

const WeekForm: React.FC<{
  onClose: () => void;
  onSubmit: () => void;
}> = ({ onClose, onSubmit }) => {
  const [intervals, setIntervals] = useState<number[]>(new Array(8).fill(0));
  const [yearStart, setYearStart] = useState<string>("");

  const handleIntervalChange = (index: number, value: string) => {
    const newIntervals = [...intervals];
    newIntervals[index] = Number(value);
    setIntervals(newIntervals);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      intervals,
      year_start: yearStart,
    };

    try {
      const response = await fetch(`${process.env.API_URL}/weeks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to add weeks");
      }

      onSubmit();
      onClose();
    } catch (error) {
      console.error("Error submitting weeks:", error);
    }
  };

  return (
    <div className="fixed z-50 inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg max-w-xl w-full">
        <h3 className="text-lg font-semibold mb-2">Adaugă săptămâni</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-1">Data inceperii anului</label>
            <input
              type="date"
              value={yearStart}
              onChange={(e) => setYearStart(e.target.value)}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Intervale</label>
            {intervals.map((interval, index) => (
              <input
                key={index}
                type="number"
                value={interval}
                onChange={(e) => handleIntervalChange(index, e.target.value)}
                className="w-full p-2 border rounded mb-2"
                required
              />
            ))}
          </div>

          <div className="flex justify-between mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-500 text-white rounded"
            >
              Închide
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Adaugă
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default WeekForm;
