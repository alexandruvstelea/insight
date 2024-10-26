"use client";
import styles from "./page.module.css";
import { useState } from "react";
import BarChartWeeks from "../barChartWeeks/page";

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
          <option value="overall">Medie Recenzii</option>
          <option value="interactivity">Recenzii Interactivitate</option>
          <option value="relevance">Recenzii Relevanță</option>
          <option value="comprehension">Recenzii Ințelegere</option>
          <option value="clarity">Recenzii Claritate</option>
        </select>
        <BarChartWeeks
          ratingsData={subjectGraphData}
          ratingType={selectedChart}
          label={
            selectedChart === "overall"
              ? "Medie Recenzii"
              : selectedChart === "interactivity"
              ? "Medie Interactivitate"
              : selectedChart === "relevance"
              ? "Medie Relevanță"
              : selectedChart === "comprehension"
              ? "Medie Ințelegere"
              : "Medie Claritate"
          }
        />
      </div>
    </>
  );
}
