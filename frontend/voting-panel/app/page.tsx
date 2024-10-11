"use server";
import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import Form from "@/components/Form";

export default async function Home() {
  return (
    <>
      <div className="flex flex-col min-h-screen">
        <NavigationBar />
        <Form />
        <Footer />
      </div>
    </>
  );
}
