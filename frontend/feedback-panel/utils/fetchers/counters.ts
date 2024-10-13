const API_URL = process.env.API_URL;

export const fetchRoomsCount = async (facultyId: number) => {
  const response = await fetch(
    `${API_URL}/rooms/count/entities?` +
      new URLSearchParams({
        faculty_id: facultyId.toString(),
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
  const roomsCount = await response.json();
  return roomsCount;
};

export const fetchProfessorsCount = async (facultyId: number) => {
  const response = await fetch(
    `${API_URL}/professors/count/entities?` +
      new URLSearchParams({
        faculty_id: facultyId.toString(),
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
  const professorsCount = await response.json();
  return professorsCount;
};

export const fetchRatingsCount = async (facultyId: number) => {
  const response = await fetch(
    `${API_URL}/ratings/count/entities?` +
      new URLSearchParams({
        faculty_id: facultyId.toString(),
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
  const ratingsCount = await response.json();
  return ratingsCount;
};
