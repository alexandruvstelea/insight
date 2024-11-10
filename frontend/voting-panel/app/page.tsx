"use server";
import LocationTransit from "@/components/LocationTransit";
import { redirect } from "next/navigation";
import { Programme } from "@/components/LocationTransit";

export default async function Home({
  searchParams,
}: {
  searchParams?: { roomCode?: string };
}) {
  if (!searchParams?.roomCode) {
    return redirect("/incorrectURL");
  }

  const roomCode = searchParams.roomCode;
  const timestamp = new Date().toISOString();

  try {
    const sessionResponse = await fetch(
      `${process.env.API_URL}/sessions/filter/current/?room_code=${roomCode}&timestamp=${timestamp}`,
      { cache: "no-store" }
    );

    if (!sessionResponse.ok) {
      throw new Error(`Session Error: ${sessionResponse.status}`);
    }

    const sessionData = await sessionResponse.json();
    const fetchedSubjectId = sessionData.subject.id;
    const fetchedSubjectName = sessionData.subject.name;

    const programmeResponse = await fetch(
      `${process.env.API_URL}/programmes/?subject_id=${fetchedSubjectId}`,
      { cache: "no-store" }
    );

    if (!programmeResponse.ok) {
      redirect("/generalError");
    }

    const programmesData = await programmeResponse.json();

    const programmes: Programme[] = programmesData.map(
      (programme: Programme) => ({
        id: programme.id,
        name: programme.name,
      })
    );
    return (
      <>
        <LocationTransit
          programmes={programmes}
          roomCode={roomCode}
          timestamp={timestamp}
          subjectName={fetchedSubjectName}
        />
      </>
    );
  } catch (error) {
    if (error instanceof Error) {
      const errorMessage = error.message;

      const statusMatch = errorMessage.match(/(\d{3})/);
      const status = statusMatch ? statusMatch[0] : "generalError";

      if (status === "404") {
        return redirect("/timestampOrRoomCodeInvalid");
      } else if (status === "500") {
        return redirect("/error500");
      } else if (status === "429") {
        return redirect("/toManyRequests");
      } else {
        return redirect("/generalError");
      }
    } else {
      return redirect("/generalError");
    }
  }
}
