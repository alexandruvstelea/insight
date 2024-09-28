"use client";

import { FC, useState } from "react";
import { Week } from "@/utils/types";
import WeekForm from "@/components/Forms/WeekForm";
import HeaderSection from "../HeaderSection";

interface WeekTableProps {
  weeks: Week[];
  fetchWeeks: () => void;
}

const WeekTable: FC<WeekTableProps> = ({ weeks = [], fetchWeeks }) => {
  const [isAddWeekModalOpen, setIsAddWeekModalOpen] = useState(false);

  const handleDeleteAll = async () => {
    if (confirm("Sigur doriți să ștergeți toate săptămânile?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/weeks`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("An error occurred while deleting weeks");
        }
        fetchWeeks();
      } catch (error) {
        alert("A apărut o eroare la ștergerea săptămânilor");
      }
    }
  };

  return (
    <>
      <div className="p-4 flex flex-col items-center justify-center glass-background">
        <HeaderSection
          title="SĂPTĂMÂNI"
          buttons={[
            {
              text: "ADAUGĂ SĂPTĂMÂNi",
              onClick: () => setIsAddWeekModalOpen(true),
            },
            {
              text: "ȘTERGE SĂPTĂMÂNI",
              onClick: handleDeleteAll,
              className: "button-red",
            },
          ]}
          count={weeks?.length || 0}
        />
        <table className="w-full text-base text-left text-gray-400">
          <thead className="text-lg  uppercase  bg-gray-700 text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Săptămâna
              </th>
              <th scope="col" className="px-6 py-3">
                Prima zi din săptămână
              </th>
              <th scope="col" className="px-6 py-3">
                Ultima zi din săptămână
              </th>
              <th scope="col" className="px-6 py-3">
                Semestru
              </th>
            </tr>
          </thead>
          <tbody>
            {weeks.length > 0 ? (
              weeks.map((week, index) => (
                <tr
                  key={week.id}
                  className="border-b bg-gray-800 border-gray-700"
                >
                  <td scope="row" className="px-6 py-4 font-medium text-white">
                    {index + 1}
                  </td>
                  <td scope="row" className="px-6 py-4 font-medium text-white">
                    {week.start}
                  </td>
                  <td scope="row" className="px-6 py-4 font-medium text-white">
                    {week.end}
                  </td>
                  <td scope="row" className="px-6 py-4 font-medium text-white">
                    {week.semester}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={4}
                  className="p-6 text-2xl text-center text-gray-500"
                >
                  Nu există săptămâni
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {isAddWeekModalOpen && (
        <WeekForm
          onClose={() => setIsAddWeekModalOpen(false)}
          onSubmit={fetchWeeks}
        />
      )}
    </>
  );
};

export default WeekTable;
