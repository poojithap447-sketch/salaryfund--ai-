import PublicNavbar from '@/components/layout/PublicNavbar'
import Footer from '@/components/layout/Footer'
import Hero from './sections/Hero'
import Stats from './sections/Stats'
import Features from './sections/Features'
import CTA from './sections/CTA'

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      <PublicNavbar />
      <Hero />
      <Stats />
      <Features />
      <CTA />
      <Footer />
    </div>
  )
}
