const API_URL = process.env.API_URL;

export const fetchFaculties = async () => {
  const response = await fetch(`${API_URL}/faculties`, {
    method: "GET",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) return false;
  const faculties = await response.json();
  return faculties;
};

export const fetchFaculty = async (facultyAbbreviation: string) => {
  const response = await fetch(
    `${API_URL}/faculties/abbreviation/${facultyAbbreviation}`,
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (!response.ok) return false;
  const faculty = await response.json();
  return faculty;
};
