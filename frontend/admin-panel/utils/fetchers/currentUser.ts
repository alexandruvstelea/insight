export const fetchCurrentUser = async (token: string) => {

  if (!token) {
    console.error("No token found");
    return false;
  }

  const response = await fetch(`${process.env.API_URL}/users/current`, {
    method: "GET",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) return false;
  const user = await response.json();
  return user;
};
