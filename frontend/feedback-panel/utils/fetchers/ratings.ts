const API_URL = process.env.API_URL;

export const fetchSubjectAverage = async (
  professorId: number,
  subjectId: number,
  subjectType: string
) => {
  const response = await fetch(
    `${API_URL}/ratings/average?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
        subject_id: subjectId.toString(),
        session_type: subjectType,
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
  const result = await response.json();
  return result;
};

export const fetchSubjectGraphData = async (
  professorId: number,
  subjectId: number,
  subjectType: string
) => {
  const response = await fetch(
    `${API_URL}/ratings/history?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
        subject_id: subjectId.toString(),
        session_type: subjectType,
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

export const fetchSubjectAveragePerProgramme = async (
  professorId: number,
  subjectId: number,
  subjectType: string
) => {
  const response = await fetch(
    `${API_URL}/ratings/average/programmes?` +
      new URLSearchParams({
        professor_id: professorId.toString(),
        subject_id: subjectId.toString(),
        session_type: subjectType,
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
  const result = await response.json();
  return result;
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
    `${API_URL}/ratings/history?` +
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
