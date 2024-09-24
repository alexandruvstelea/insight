import React, { useState } from "react";
import ButtonGroup from "../ButtonGroup";

const WeekForm: React.FC<{
  onClose: () => void;
  onSubmit: () => void;
}> = ({ onClose, onSubmit }) => {
  const [intervals, setIntervals] = useState<number[]>(new Array(8).fill(""));
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
    <div className="fixed z-50 inset-0 bg-gray-800 bg-opacity-75 flex justify-center items-center">
      <div className="bg-slate-700 p-4 rounded shadow-lg max-w-xl w-full max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-semibold text-center mb-2 text-white">
          Adaugă săptămâni
        </h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="yearStart" className="label">
              Data inceperii anului *
            </label>
            <input
              id="yearStart"
              type="date"
              value={yearStart}
              onChange={(e) => setYearStart(e.target.value)}
              className="input"
              required
            />
          </div>
          {intervals.map((interval, index) => (
            <div key={index} className="mb-4">
              <label className="label">
                Numar saptamani interval {index + 1} *
              </label>

              <input
                key={index}
                type="number"
                value={interval}
                onChange={(e) => handleIntervalChange(index, e.target.value)}
                className="input"
                required
              />
            </div>
          ))}
          <ButtonGroup onClose={onClose} />
        </form>
      </div>
    </div>
  );
};

export default WeekForm;
