"use server";

import Desboard from "@/components/Deshboard";
import { fetchCurrentUser } from "@/utils/fetchers/currentUser";

export default async function Home() {
  const currentUser = await fetchCurrentUser();
  console.log(currentUser);

  return (
    <>
      <Desboard />
    </>
  );
}
