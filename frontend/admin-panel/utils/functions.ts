export const weekTypeMapping: Record<number, string> = {
<<<<<<< HEAD
  0: "Par și impar",
=======
  0: "Ambele",
>>>>>>> 2f8964e (Almost finished the admin page.)
  1: "Impar",
  2: "Par",
};

export const dayMapping = [
  "Luni",
  "Marți",
  "Miercuri",
  "Joi",
  "Vineri",
  "Sâmbătă",
  "Duminică",
];

export  const sessionTypeMapping = {
  course: "Curs",
  seminar: "Seminar",
  laboratory: "Laborator",
  project: "Proiect",
};

export  const programmeTypeMapping = {
  bachelor: "Licență",
  master: "Master",
  phd: "Doctorat",
};
export  const genderTypeMapping = {
  male: "Masculin",
  female: "Feminin",
};

export const genderOptions = [
  { value: "male", label: "Masculin" },
  { value: "female", label: "Feminin" },
];
export const semesterOptions = [
  { value: 1, label: "1" },
  { value: 2, label: "2" },
];

export const startEndTimeOptions = [
  "08:00",
  "10:00",
  "12:00",
  "14:00",
  "16:00",
  "18:00",
  "20:00",
  "22:00",
].map((time) => ({ value: time, label: time }));

export const formatTimeForDisplay = (time: string) => {
  return time.slice(0, 5); 
};

export const formatTimeForBackend = (time: string) => {
  return `${time}:00`; 
};