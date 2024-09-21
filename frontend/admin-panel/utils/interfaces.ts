import { Faculty, Building,Room,Session,Comment, Professor, Programme,Week, Subject } from "@/utils/types";

export interface FacultyTableProps {
  faculties: Faculty[];
  buildings: Building[];
  professors: Professor[];
  programmes: Programme[];
  fetchFaculties: () => Promise<void>;
}

export interface RoomTableProps {
  rooms: Room[];
  buildings: Building[];
  sessions: Session[];
  fetchRooms: () => Promise<void>;
}

export interface BuildingTableProps {
  buildings: Building[];
  rooms: Room[];
  faculties: Faculty[];
  fetchBuildings: () => Promise<void>;
}

export interface ProgrammeTableProps {
  programmes: Programme[];
  faculties: Faculty[];
  subjects: Subject[];
  fetchProgrammes: () => Promise<void>;
}

export interface SessionTableProps {
  sessions: Session[];
  rooms: Room[];
  faculties:Faculty[];
  subjects: Subject[];
  fetchSessions: () => Promise<void>;
}
export interface ProfessorTableProps {
  professors: Professor[];
  faculties: Faculty[];
  fetchProfessors: () => Promise<void>;
}
export interface SubjectTableProps {
  subjects: Subject[];
  programmes: Programme[];
  professors:Professor[];
  sessions:Session[];
  fetchSubjects: () => Promise<void>;
}
export interface WeekTableProps {
  weeks: Week[];
  fetchWeeks: () => Promise<void>;
}

export interface CommentTableProps {
  comments: Comment[] | null | undefined;
  fetchComments: () => void;
}



export interface HeaderSectionProps {
  title: string;
  buttons?: { text: string; onClick: () => void; className?: string }[];
  count: number;
}