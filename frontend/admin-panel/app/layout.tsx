import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://admin.insightbv.ro"),
  openGraph: {
    title: "inSight Admin Panel",
    description:
      "Acesta este panoul de administrare al proiectului inSight. De aici, se realizează operațiuni CRUD și se monitorizează activitatea aplicației pentru o administrare eficientă.",
    url: "https://admin.insightbv.ro",
    siteName: "admin.insightbv.ro",
    images: [
      {
        url: "/pngs/social-share.png",
        width: 800,
        height: 600,
      },
    ],
    locale: "ro_RO",
    type: "website",
  },
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
