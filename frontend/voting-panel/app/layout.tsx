import type { Metadata } from "next";
import "./globals.css";
import { Montserrat } from "next/font/google";
import Footer from "@/components/Footer";
import ReportBanner from "@/components/ReportBanner";
import NavigationBar from "@/components/NavigationBar";

const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://voting.insightbv.ro"),
  openGraph: {
    title: "inSight Voting Panel",
    description:
      "Acesta este panoul de votare al platformei inSight, unde studenții își pot ajuta profesorii oferindu-le feedback constructiv legat de cursurile lor.",
    url: "https://voting.insightbv.ro",
    siteName: "voting.insightbv.ro",
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
    <html className="bg-black" lang="en">
      <body className={`${montserrat.className} antialiased bg-white`}>
        <div className="flex flex-col min-h-screen justify-between ">
          <NavigationBar />

          {children}
          <div className="relative">
            <ReportBanner />
            <Footer />
          </div>
        </div>
      </body>
    </html>
  );
}
