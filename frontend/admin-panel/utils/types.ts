export type Faculty = {
  id: number;
  name: string;
  abbreviation: string;
  buildings: Building[];
  professors: Professor[];
  programmes: Programme[];
};

export type Building = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  rooms: Room[];
  faculties: Faculty[];
};

export type Room = {
  id: number;
  name: string;
  building: Building;
  sessions: Session[];
};

export type Programme = {
  id: number;
  name: string;
  abbreviation: string;
  type: "bachelor" | "master" | "phd";
  faculty: Faculty;
  subjects: Subject[];
};

export type Professor = {
  id: number;
  first_name: string;
  last_name: string;
  gender: "male" | "female";
  faculties: Faculty[];
  courses: SessionType[];
  laboratories: SessionType[];
  seminars: SessionType[];
  projects: SessionType[];
};

export type SessionType = {
  id: number;
  name: string;
  abbreviation: string;
  semester: number;
  course_professor_id: number;
  laboratory_professor_id: number;
  seminar_professor_id: number;
  project_professor_id: number;
};

export type Subject = {
  id: number;
  name: string;
  abbreviation: string;
  semester: 1 | 2;
  course_professor_id: number;
  laboratory_professor_id: number;
  seminar_professor_id: number;
  project_professor_id: number;
  programmes: Programme[];
  sessions: Session[];
  course_professor: Professor;
  laboratory_professor: Professor;
  seminar_professor: Professor;
  project_professor: Professor;
};

export type Session = {
  id: number;
  type: "course" | "laboratory" | "seminar" | "project";
  semester: 1 | 2;
  week_type: 0 | 1 | 2;
  start: string;
  end: string;
  day: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  faculty_ids: number[];
  room: Room;
  subject: Subject;
};

export type Week = {
  id: number;
  start: string;
  end: string;
  semester: number;
};

export type Comment = {
  id: number;
  text: string;
  timestamp: string;
  room_id: Room[];
  programme_id: Programme[];
  subject_id: Subject[];
  professor_id: Professor[];
  faculty_id: Faculty[];
  roomName: string;
  programmeName: string;
  subjectName: string;
  professorName: string;
  facultyName: string;
};

export type Rating = {
  id: number;
  rating_clarity: number;
  rating_interactivity: number;
  rating_relevance: number;
  rating_comprehension: number;
  rating_overall: number;
  timestamp: string;
  session_type: string;
  subject_id: number;
  programme_id: number;
  professor_id: number;
  faculty_id: number;
  room_id: number;
};

export type User = {
  id: number;
  email: string;
  role: "admin" | "tablet";
};
