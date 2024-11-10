import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import { Footer } from "@/components/footer/page";
import IssueReport from "@/components/issueReport/page";

const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://insightbv.ro"),
  openGraph: {
    title: "inSight",
    description:
      "InSight este un proiect creat pentru a facilita comunicarea dintre studenți și profesori în cadrul Universității Transilvania din Brașov, oferindu-le profesorilor un feedback constructiv despre cursurile lor.",
    url: "https://insightbv.ro",
    siteName: "insightbv.ro",
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
    <>
      <html lang="en">
        <body className={`${montserrat.className} layoutBody`}>
          <div className="layoutContainer">
            {children}
            <Footer />
          </div>
          <IssueReport />
        </body>
      </html>
    </>
  );
}
