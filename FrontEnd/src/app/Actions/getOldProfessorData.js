"use server";

const fetchOldProfessorSubjects = async (professorId, selectedYear) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/subjects/professors_archive/${selectedYear}/${professorId}`,
    { cache: "no-store" }
  );
  if (!response.ok) return [];
  const subjects = await response.json();
  return subjects;
};

const fetchOldProfessorAverage = async (professorId, selectedYear) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/professors/average_archive/${selectedYear}/${professorId}`,
    { cache: "no-store" }
  );
  if (!response.ok) return "N/A";
  const average = await response.json();
  return average.average;
};

export const fetchOldProfessorsData = async (selectedYear) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/professors_archive/${selectedYear}`,
    {
      cache: "no-store",
    }
  );
  if (!response.ok) return false;
  const professors = await response.json();

  const fetchPromises = professors.map(async (professor) => {
    const [subjects, average] = await Promise.all([
      fetchOldProfessorSubjects(professor.id),
      fetchOldProfessorAverage(professor.id),
    ]);
    return { ...professor, subjects, average };
  });

  const updatedProfessors = await Promise.all(fetchPromises);
  return updatedProfessors;
};
