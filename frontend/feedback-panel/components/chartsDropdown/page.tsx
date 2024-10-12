"use client";
import styles from "./page.module.css";
import { useState } from "react";
import BarChart from "../barChart/page";

type ChartType =
  | "overall"
  | "interactivity"
  | "relevance"
  | "comprehension"
  | "clarity";

interface ChartsDropdownProps {
  subjectGraphData: any;
}

export default function ChartsDropdown({
  subjectGraphData,
}: ChartsDropdownProps) {
  const [selectedChart, setSelectedChart] = useState<ChartType>("overall");

  const handleChartChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedChart(event.target.value as ChartType);
  };

  return (
    <>
      <div className={styles.dropdownContainer}>
        <select
          value={selectedChart}
          onChange={handleChartChange}
          className={styles.dropdown}
        >
          <option value="overall">Istoric Medie Recenzii</option>
          <option value="interactivity">
            Istoric Recenzii Interactivitate
          </option>
          <option value="relevance">Istoric Recenzii Relevanta</option>
          <option value="comprehension">Istoric Recenzii Intelegere</option>
          <option value="clarity">Istoric Recenzii Claritate</option>
        </select>
        <BarChart
          ratingsData={subjectGraphData}
          ratingType={selectedChart}
          label={
            selectedChart === "overall"
              ? "Medie Recenzii"
              : selectedChart === "interactivity"
              ? "Medie Interactivitate"
              : selectedChart === "relevance"
              ? "Medie Relevanta"
              : selectedChart === "comprehension"
              ? "Medie Intelegere"
              : "Medie Claritate"
          }
        />
      </div>
    </>
  );
}
