import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import { NavigationBar } from "@/components/navigationBar/page";
import { Footer } from "@/components/footer/page";

const inter = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "inSight",
  description:
    "This is the feedback panel of the Feedback UnitBV project. Here you can see the ratings that each professors has received from their students.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <html lang="en">
        <body className={inter.className}>
          {children}
          <Footer />
        </body>
      </html>
    </>
  );
}
