"use server";

export const fetchGraphData = async (subjectId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/graph?subject_id=${subjectId}`,
    {
      cache: "no-store",
    }
  );
  if (!response.ok) return false;
  const graphData = await response.json();

  return graphData;
};
