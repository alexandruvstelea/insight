const API_URL = process.env.API_URL;

export const fetchProfessor = async (professorId: number) => {
  const response = await fetch(`${API_URL}/professors/${professorId}`, {
    method: "GET",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) return false;
  const professor = await response.json();
  return professor;
};

export const fetchProfessorAvgRating = async (professorId: number) => {
  const response = await fetch(
    `${API_URL}/ratings/average?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
      }),
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (!response.ok) return false;
  const avgRating = await response.json();
  return avgRating;
};

export const fetchProfessorRatingsHistory = async (professorId: number) => {
  const response = await fetch(
    `${API_URL}/ratings/graph?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
      }),
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) return false;
  const graphData = await response.json();
  return graphData;
};
