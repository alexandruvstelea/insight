import { Faculty, Building, Room, Session, Comment, Professor, Programme, Week, Subject } from "@/utils/types";

export interface FacultyTableProps {
  faculties: Faculty[] | null | undefined;
  buildings: Building[] | null | undefined;
  professors: Professor[] | null | undefined;
  programmes: Programme[] | null | undefined;
  fetchFaculties: () => Promise<void>;
}

export interface RoomTableProps {
  rooms: Room[] | null | undefined;
  buildings: Building[] | null | undefined;
  sessions: Session[] | null | undefined;
  fetchRooms: () => Promise<void>;
}

export interface BuildingTableProps {
  buildings: Building[] | null | undefined;
  rooms: Room[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  fetchBuildings: () => Promise<void>;
}

export interface ProgrammeTableProps {
  programmes: Programme[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  subjects: Subject[] | null | undefined;
  fetchProgrammes: () => Promise<void>;
}

export interface SessionTableProps {
  sessions: Session[] | null | undefined;
  rooms: Room[] | null | undefined;
  faculties:Faculty[] | null | undefined;
  subjects: Subject[] | null | undefined;
  fetchSessions: () => Promise<void>;
}
export interface ProfessorTableProps {
  professors: Professor[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  fetchProfessors: () => Promise<void>;
}
export interface SubjectTableProps {
  subjects: Subject[] | null | undefined;
  programmes: Programme[] | null | undefined;
  professors: Professor[] | null | undefined;
  sessions: Session[] | null | undefined;
  fetchSubjects: () => Promise<void>;
}
export interface WeekTableProps {
  weeks: Week[] | null | undefined;
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