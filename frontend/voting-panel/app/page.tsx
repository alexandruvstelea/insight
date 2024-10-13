"use server";
import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import LocationTransit from "@/components/LocationTransit";
import { redirect } from "next/navigation";

export default async function Home({
  searchParams,
}: {
  searchParams?: { roomCode?: string };
}) {
  if (!searchParams || !searchParams.roomCode) {
    return redirect("https://www.google.com");
  }

  const roomCode = searchParams.roomCode;
  const timestamp = "2023-10-02T10:35:59.961Z";

  try {
    const sessionResponse = await fetch(
      `${process.env.API_URL}/sessions/filter/current?room_code=${roomCode}&timestamp=${timestamp}`
    );

    if (!sessionResponse.ok) {
      if (sessionResponse.status === 404) {
        redirect("https://www.google.com");
      } else {
        throw new Error(
          `Error fetching session: ${sessionResponse.statusText}`
        );
      }
    }
    const sessionData = await sessionResponse.json();
    const fetchedSubjectId = sessionData.subject.id;

    const programmeResponse = await fetch(
      `${process.env.API_URL}/programmes?subject_id=${fetchedSubjectId}`
    );

    if (!programmeResponse.ok) {
      throw new Error(
        `Error fetching programmes: ${programmeResponse.statusText}`
      );
    }

    const programmesData = await programmeResponse.json();
    const programmes = programmesData.map((programme: any) => ({
      id: programme.id,
      name: programme.name,
    }));

    return (
      <>
        <div className="flex flex-col min-h-screen justify-between">
          <NavigationBar />
          <LocationTransit
            programmes={programmes}
            roomCode={roomCode}
            timestamp={timestamp}
          />
          <Footer />
        </div>
      </>
    );
  } catch (error) {
    console.error("Error:", error);
    return redirect("https://www.google.com");
  }
}
