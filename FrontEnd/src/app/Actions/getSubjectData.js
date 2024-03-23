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
export const fetchRatingsAverageData = async (subjectId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/rating/${subjectId}`,
    {
      cache: "no-store",
    }
  );
  if (!response.ok) return false;
  const ratingsAverage = await response.json();

  return ratingsAverage;
};

export const fetchProgrammesData = async () => {
  const response = await fetch(`${process.env.REACT_APP_API_URL}/programmes`, {
    cache: "no-store",
  });
  if (!response.ok) return false;
  const programmes = await response.json();

  return programmes;
};

export const fetchCommentsData = async (subjectId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/comments/${subjectId}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) return [];
  const comments = await response.json();

  return comments;
};
