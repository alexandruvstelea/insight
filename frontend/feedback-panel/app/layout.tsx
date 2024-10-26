import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import { Footer } from "@/components/footer/page";

const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "inSight",
  description:
    "InSight este un proiect creat cu scopul de a facilita comunicarea dintre studenți și profesori in cadrul Universitatii Transilvania din Brasov, pentru a le oferi profesorilor un feedback constructiv asupra cursurilor lor.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <html lang="en">
        <body className={`${montserrat.className} layoutBody`}>
          <div className="layoutContainer">
            {children}
            <Footer />
          </div>
        </body>
      </html>
    </>
  );
}
