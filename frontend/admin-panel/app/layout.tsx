import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "inSight Admin Panel",
  description:
    "This is the inSight admin panel used to perform operations on the database",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="bg-slate-900 min-h-screen">{children}</div>
      </body>
    </html>
  );
}
