"use client";

import { FC, useState } from "react";
import { BugReportTableProps } from "@/utils/interfaces";
import TableActions from "@/components/TableActions";
import HeaderSection from "@/components/HeaderSection";
import SuccessToast from "@/components/SuccessToast";
import ErrorToast from "@/components/ErrorToast";

const BugReportTable: FC<BugReportTableProps> = ({
  bugReports = [],
  fetchBugReports,
}) => {
  const [showSuccessToast, setShowSuccessToast] = useState(false);
  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleDelete = async (id: number) => {
    if (confirm("Sigur doriți să ștergeți acest bug report?")) {
      try {
        const response = await fetch(`${process.env.API_URL}/reports/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("A apărut o eroare la ștergerea bug report-ului");
        }
        setShowSuccessToast(true);
        fetchBugReports();
      } catch (error: any) {
        setErrorMessage(error.message);
        setShowErrorToast(true);
      }
    }
  };

  return (
    <div className="p-4 flex flex-col items-center justify-center glass-background">
      <HeaderSection
        title="Reporturi"
        count={bugReports?.length || 0}
        buttons={[]}
      />
      <table className="w-full text-base text-left text-gray-400">
        <thead className="text-lg uppercase bg-gray-700 text-gray-400">
          <tr>
            <th scope="col" className="px-6 py-3">
              Acțiuni
            </th>
            <th scope="col" className="px-6 py-3">
              Text
            </th>
            <th scope="col" className="px-6 py-3">
              Timestamp
            </th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(bugReports) && bugReports.length > 0 ? (
            bugReports.map((bugReport) => (
              <tr
                key={bugReport.id}
                className="border-b bg-gray-800 border-gray-700"
              >
                <TableActions
                  onDelete={() => handleDelete(bugReport.id)}
                  showEdit={false}
                />
                <td scope="row" className="px-6 py-4 font-medium text-white">
                  {bugReport.text}
                </td>
                <td scope="row" className="px-6 py-4 font-medium text-white">
                  {bugReport.timestamp}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={8}
                className="p-6 text-2xl text-center text-gray-500"
              >
                Nu există reporturi
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {showSuccessToast && (
        <SuccessToast
          message="Bug report-ul a fost șters cu succes."
          onClose={() => setShowSuccessToast(false)}
        />
      )}

      {showErrorToast && (
        <ErrorToast
          message={errorMessage}
          onClose={() => setShowErrorToast(false)}
        />
      )}
    </div>
  );
};

export default BugReportTable;
