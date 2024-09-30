"use server";

import Desboard from "@/components/Deshboard";
import MobileWarning from "@/components/MobileWarning";
export default async function Home() {
  return (
    <>
      <Desboard />
      <MobileWarning />
    </>
  );
}
