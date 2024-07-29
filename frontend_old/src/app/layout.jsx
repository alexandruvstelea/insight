import { Montserrat } from "next/font/google";
import "./globals.css";
import { GoogleAnalytics } from "@next/third-parties/google";
const montserrat = Montserrat({ subsets: ["latin"] });

export const metadata = {
  metadataBase: new URL("https://feedbackiesc.ro"),
  openGraph: {
    title: "Feedback IESC",
    description: "Părerea ta contează",
    url: "https://feedbackiesc.ro",
    siteName: "feedbackiesc.ro",
    images: [
      {
        url: "/social-share.png",
        width: 800,
        height: 600,
      },
    ],
    locale: "ro_RO",
    type: "website",
  },
  content: "width=device-width, initial-scale=1.0",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={montserrat.className}>{children}</body>
      <GoogleAnalytics gaId={process.env.GOOGLE_ANALYTICS} />
    </html>
  );
}
