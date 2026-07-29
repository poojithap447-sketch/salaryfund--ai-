import PublicNavbar from '@/components/layout/PublicNavbar'
import Footer from '@/components/layout/Footer'
import ScrollReveal from '@/components/animations/ScrollReveal'
import { Card, CardContent } from '@/components/ui/card'
import AnimatedCounter from '@/components/animations/AnimatedCounter'

const VALUES = [
  { title: 'Trust first', desc: 'Every score, every rate, every decision is explainable — to employees and regulators alike.' },
  { title: 'Speed without shortcuts', desc: 'Sub-minute disbursals, backed by real underwriting, not gimmicks.' },
  { title: 'Built for scale', desc: 'From a 50-person startup to a 50,000-person enterprise, on the same platform.' },
]

export default function About() {
  return (
    <div className="min-h-screen bg-background">
      <PublicNavbar />

      <section className="bg-mesh py-24">
        <div className="container">
          <ScrollReveal className="mx-auto max-w-2xl text-center">
            <span className="text-xs font-medium uppercase tracking-widest text-primary">About us</span>
            <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight">
              We're rebuilding how people access their own money.
            </h1>
            <p className="mt-4 text-muted-foreground">
              SalaryFund AI was founded to close the gap between when people earn and when they get paid —
              using AI-driven risk models instead of predatory short-term credit.
            </p>
          </ScrollReveal>
        </div>
      </section>

      <section className="py-20">
        <div className="container grid grid-cols-1 gap-5 sm:grid-cols-3">
          {VALUES.map((v, idx) => (
            <ScrollReveal key={v.title} delay={idx * 0.1}>
              <Card className="h-full">
                <CardContent className="p-6">
                  <h3 className="font-display text-lg font-semibold">{v.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{v.desc}</p>
                </CardContent>
              </Card>
            </ScrollReveal>
          ))}
        </div>
      </section>

      <section className="border-y border-white/[0.06] bg-surface/40 py-16">
        <div className="container flex flex-col items-center gap-2 text-center">
          <p className="font-display text-4xl font-semibold">
            <AnimatedCounter value={64} suffix="+" />
          </p>
          <p className="text-sm text-muted-foreground">Enterprises trust SalaryFund AI with their payroll</p>
        </div>
      </section>

      <Footer />
    </div>
  )
}
