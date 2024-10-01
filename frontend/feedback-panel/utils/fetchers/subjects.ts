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
  courses: { id: number; name: string; abbreviation: string }[];
  laboratories: { id: number; name: string; abbreviation: string }[];
  seminars: { id: number; name: string; abbreviation: string }[];
  projects: { id: number; name: string; abbreviation: string }[];
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

  if (Array.isArray(result)) {
    result.forEach((subject: Subject) => {
      const subjectInfo = {
        id: subject.id,
        name: subject.name,
        abbreviation: subject.abbreviation,
      };

      if (subject.course_professor_id == professorId)
        professorSubjects.courses.push(subjectInfo);
      if (subject.laboratory_professor_id == professorId)
        professorSubjects.laboratories.push(subjectInfo);
      if (subject.seminar_professor_id == professorId)
        professorSubjects.seminars.push(subjectInfo);
      if (subject.project_professor_id == professorId)
        professorSubjects.projects.push(subjectInfo);
    });
  } else {
    console.error("Invalid input data: result should be an array.");
  }
  return professorSubjects;
};
