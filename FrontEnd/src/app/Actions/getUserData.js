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
