"use server";

export const fetchOldGraphData = async (subjectId, year) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/graph_archive/${year}?subject_id=${subjectId}`,
    {
      cache: "no-store",
    }
  );
  if (!response.ok) return false;
  const graphData = await response.json();

  return graphData;
};
export const fetchOldRatingsAverageData = async (subjectId, year) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/rating_archive/${year}/${subjectId}`,
    {
      cache: "no-store",
    }
  );
  if (!response.ok) return false;
  const ratingsAverage = await response.json();

  return ratingsAverage;
};

export const fetchOldCommentsData = async (subjectId, year) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/comments_archive/${year}/${subjectId}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) return [];
  const comments = await response.json();

  return comments;
};

export const fetchOldDescriptionData = async (subjectId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/subjects/description/${subjectId}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) return false;
  const description = await response.json();

  return description;
};
