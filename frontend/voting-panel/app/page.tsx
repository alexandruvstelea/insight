"use server";
import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import LocationTransit from "@/components/LocationTransit";

export default async function Home() {
  return (
    <>
      <div className="flex flex-col min-h-screen justify-between">
        <NavigationBar />
        <LocationTransit />
        <Footer />
      </div>
    </>
  );
}
