import type { Metadata } from "next";
import "./globals.css";
import { Montserrat } from "next/font/google";

const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "inSight",
  description: "This is the voting panel of the Feedback UnitBV project.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html className="bg-black" lang="en">
      <body className={`${montserrat.className} antialiased bg-white`}>
        {children}
      </body>
    </html>
  );
}
