<<<<<<< HEAD
import { Faculty, Building, Room, Session, Comment, Professor, Programme, Week, Subject, User } from "@/utils/types";

export interface FacultyTableProps {
  faculties: Faculty[] | null | undefined;
  buildings: Building[] | null | undefined;
  professors: Professor[] | null | undefined;
  programmes: Programme[] | null | undefined;
=======
import { Faculty, Building,Room,Session,Comment, Professor, Programme,Week, Subject } from "@/utils/types";

export interface FacultyTableProps {
  faculties: Faculty[];
  buildings: Building[];
  professors: Professor[];
  programmes: Programme[];
>>>>>>> 2f8964e (Almost finished the admin page.)
  fetchFaculties: () => Promise<void>;
}

export interface RoomTableProps {
<<<<<<< HEAD
  rooms: Room[] | null | undefined;
  buildings: Building[] | null | undefined;
  sessions: Session[] | null | undefined;
=======
  rooms: Room[];
  buildings: Building[];
  sessions: Session[];
>>>>>>> 2f8964e (Almost finished the admin page.)
  fetchRooms: () => Promise<void>;
}

export interface BuildingTableProps {
<<<<<<< HEAD
  buildings: Building[] | null | undefined;
  rooms: Room[] | null | undefined;
  faculties: Faculty[] | null | undefined;
=======
  buildings: Building[];
  rooms: Room[];
  faculties: Faculty[];
>>>>>>> 2f8964e (Almost finished the admin page.)
  fetchBuildings: () => Promise<void>;
}

export interface ProgrammeTableProps {
<<<<<<< HEAD
  programmes: Programme[] | null | undefined;
  faculties: Faculty[] | null | undefined;
  subjects: Subject[] | null | undefined;
=======
  programmes: Programme[];
  faculties: Faculty[];
  subjects: Subject[];
>>>>>>> 2f8964e (Almost finished the admin page.)
  fetchProgrammes: () => Promise<void>;
}

export interface SessionTableProps {
<<<<<<< HEAD
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
=======
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
>>>>>>> 2f8964e (Almost finished the admin page.)
  fetchWeeks: () => Promise<void>;
}

export interface CommentTableProps {
  comments: Comment[] | null | undefined;
  fetchComments: () => void;
}
<<<<<<< HEAD
export interface UserTableProps {
  users: User[] | null | undefined;
  fetchUsers: () => void;
}
=======
>>>>>>> 2f8964e (Almost finished the admin page.)



export interface HeaderSectionProps {
  title: string;
  buttons?: { text: string; onClick: () => void; className?: string }[];
  count: number;
<<<<<<< HEAD
}

export interface ModalProps<T> {
  items: T[];
  title: string;
  onClose: () => void;
  renderItem: (item: T) => React.ReactNode;
  isTable?: boolean;
}

export interface ButtonGroupProps {
  onClose: () => void;
  isEditMode?: boolean;
=======
>>>>>>> 2f8964e (Almost finished the admin page.)
}