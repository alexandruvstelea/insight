import { Montserrat } from 'next/font/google'
import './globals.css'
import { GoogleAnalytics } from '@next/third-parties/google'
const montserrat = Montserrat({ subsets: ['latin'] })

export const metadata = {
  title: 'Feedback IESC',
  name: "viewport",
  content: "width=device-width, initial-scale=1.0"
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={montserrat.className} >{children}
      </body>
      <GoogleAnalytics gaId={process.env.GOOGLE_ANALYTICS} />
    </html>
  )
}