import { NextApiRequest } from "next";

const API_URL = process.env.API_URL;

export const fetchFaculties = async (req: NextApiRequest) => {
  let clientIp = req.headers["x-forwarded-for"] || req.socket.remoteAddress;

  if (Array.isArray(clientIp)) {
    clientIp = clientIp.join(", ");
  } else if (clientIp === undefined) {
    clientIp = "";
  }

  const response = await fetch(`${process.env.API_URL}/faculties`, {
    method: "GET",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      "X-Forwarded-For": clientIp,
    },
  });

  if (!response.ok) return false;

  const faculties = await response.json();
  return faculties;
};

export const fetchFaculty = async (facultyAbbreviation: string) => {
  const response = await fetch(
    `${API_URL}/faculties/abbreviation/${facultyAbbreviation}`,
    {
      method: "GET",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (!response.ok) return false;
  const faculty = await response.json();
  return faculty;
};
