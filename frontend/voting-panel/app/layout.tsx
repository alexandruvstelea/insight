import type { Metadata } from "next";
import "./globals.css";
import { Montserrat } from "next/font/google";
import Footer from "@/components/Footer";
import ReportBanner from "@/components/ReportBanner";
import NavigationBar from "@/components/NavigationBar";

const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "inSight Voting Panel",
  description: "This is the voting panel of the inSight project.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html className="bg-black" lang="en">
      <body className={`${montserrat.className} antialiased bg-white`}>
        <div className="flex flex-col min-h-screen justify-between ">
          <div className="relative">
            <ReportBanner />
            <NavigationBar />
          </div>
          {children}
          <Footer />
        </div>
      </body>
    </html>
  );
}
