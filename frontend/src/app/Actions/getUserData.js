"use client";
export const fetchCheckLogin = async () => {
  const response = await fetch(`${process.env.REACT_APP_API_URL}/check-login`, {
    cache: "no-store",
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) return false;
  const loggedIn = await response.json();

  return loggedIn;
};

export const fetchLogoutUser = async () => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/logout`, {
      method: "GET",
      credentials: "include",
    });
    if (response.ok) {
      console.log("Logout successful");
      return true;
    } else {
      console.error("Logout failed:", response.statusText);
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};
