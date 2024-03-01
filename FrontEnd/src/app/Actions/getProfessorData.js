"use server";

const fetchProfessorSubjects = async (professorId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/subjects/professor/${professorId}`,
    { cache: "no-store" }
  );
  if (!response.ok) return [];
  const subjects = await response.json();
  return subjects;
};

const fetchProfessorAverage = async (professorId) => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/professors/average/${professorId}`,
    { cache: "no-store" }
  );
  if (!response.ok) return "N/A";
  const average = await response.json();
  return average.average;
};

export const fetchProfessorsData = async () => {
  const response = await fetch(`${process.env.REACT_APP_API_URL}/professors`, {
    cache: "no-store",
  });
  if (!response.ok) return false;
  const professors = await response.json();
  for (const professor of professors) {
    const subjects = await fetchProfessorSubjects(professor.id);
    const average = await fetchProfessorAverage(professor.id);
    professor.subjects = subjects;
    professor.average = average;
  }
  return professors;
};

// export const fetchProfessorsData = async () => {
//   const response = await fetch(`${process.env.REACT_APP_API_URL}/professors`, {
//     cache: "no-store",
//   });
//   if (!response.ok) return false;
//   const professors = await response.json();

//   const fetchPromises = professors.map(async (professor) => {
//     const [subjects, average] = await Promise.all([
//       fetchProfessorSubjects(professor.id),
//       fetchProfessorAverage(professor.id)
//     ]);
//     return { ...professor, subjects, average };
//   });

//   const updatedProfessors = await Promise.all(fetchPromises);
//   console.log(updatedProfessors);
//   return updatedProfessors;
// };
