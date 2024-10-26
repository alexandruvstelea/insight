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

export const transformProfessorName = (
  lastName: string,
  firstName: string
): string => {
  const fullName = `${lastName} ${firstName}`;
  return fullName.toLowerCase().replace(/\s+/g, "-");
};

export const reverseTransformName = (
  transformedName: string
): { firstName: string; lastName: string } => {
  const decodedName = decodeURIComponent(transformedName);

  const parts = decodedName.split("-");

  const capitalizedParts = parts.map(
    (word) => word.charAt(0).toUpperCase() + word.slice(1)
  );

  const lastName = capitalizedParts[0];
  const firstName = capitalizedParts.slice(1).join(" ");

  return { firstName, lastName };
};
