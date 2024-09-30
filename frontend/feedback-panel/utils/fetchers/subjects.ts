const API_URL = process.env.API_URL;

interface Subject {
  id: number;
  name: string;
  abbreviation: string;
  semester: 1 | 2;
  course_professor_id?: number | null;
  laboratory_professor_id?: number | null;
  seminar_professor_id?: number | null;
  project_professor_id?: number | null;
}

export interface ProfessorSubjects {
  courses: string[];
  laboratories: string[];
  seminars: string[];
  projects: string[];
}

export const fetchSubjectsByProfessor = async (professorId: number) => {
  const response = await fetch(
    `${API_URL}/subjects/?` +
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
  const result = await response.json();
  let professorSubjects: ProfessorSubjects = {
    courses: [],
    laboratories: [],
    seminars: [],
    projects: [],
  };
  if (Array.isArray(result))
    result.forEach((subject: Subject) => {
      if (subject.course_professor_id == professorId)
        professorSubjects.courses.push(subject.name);
      if (subject.laboratory_professor_id == professorId)
        professorSubjects.laboratories.push(subject.name);
      if (subject.seminar_professor_id == professorId)
        professorSubjects.seminars.push(subject.name);
      if (subject.project_professor_id == professorId)
        professorSubjects.projects.push(subject.name);
    });
  else
    console.error(
      "Invalid input data: result.array should be an array and professorSubjects.courses should be an array."
    );

  return professorSubjects;
};
