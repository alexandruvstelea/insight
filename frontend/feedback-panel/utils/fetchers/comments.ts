const API_URL = process.env.API_URL;

export const fetchSubjectComments = async (
  professorId: number,
  subjectId: number,
  subjectType: string
) => {
  const response = await fetch(
    `${API_URL}/comments?` +
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
