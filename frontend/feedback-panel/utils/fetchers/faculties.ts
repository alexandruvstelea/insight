const API_URL = process.env.API_URL;

export const fetchFaculties = async () => {
  const response = await fetch(`${API_URL}/faculties`, { cache: "no-store" });
  if (!response.ok) return false;
  const faculties = await response.json();
  return faculties;
};

export const fetchFaculty = async (facultyID: number) => {
  const response = await fetch(`${API_URL}/faculties/${facultyID}`, {
    cache: "no-store",
  });
  if (!response.ok) return false;
  const faculty = await response.json();
  return faculty;
};
