const API_URL = process.env.API_URL;

export const fetchProfessor = async (firstName: string, lastName: string) => {
  const response = await fetch(
    `${API_URL}/professors/name/filter?` +
      new URLSearchParams({
        first_name: firstName,
        last_name: lastName,
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

export const transformProfessorName = (
  lastName: string,
  firstName: string
): string => {
  const removeSpecialChars = (str: string): string => {
    return str
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "") // Remove diacritics
      .replace(/[^a-zA-Z0-9\s-]/g, ""); // Remove special characters
  };

  const fullName = `${lastName} ${firstName}`;
  const sanitizedFullName = removeSpecialChars(fullName);

  return sanitizedFullName.toLowerCase().replace(/\s+/g, "-");
};

export const reverseTransformName = (
  transformedName: string
): { firstName: string; lastName: string } => {
  const parts = transformedName.split("-");

  const capitalizedParts = parts.map(
    (word) => word.charAt(0).toUpperCase() + word.slice(1)
  );

  const lastName = capitalizedParts[0];
  const firstName = capitalizedParts.slice(1).join(" ");

  return { firstName, lastName };
};
