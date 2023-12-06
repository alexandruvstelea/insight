import Footer from '@/components/Footer'
import Header from '@/components/Header'

export default function CourseLayout({ children }) {
  return (
    <>
      <Header />
      {children}
      <Footer />
    </>
  )

}