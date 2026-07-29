import { BarChart3, Gauge, ShieldCheck, Wallet, Zap, PiggyBank } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import ScrollReveal from '@/components/animations/ScrollReveal'

const FEATURES = [
  { icon: Zap, title: 'Instant salary advance', desc: 'Employees draw up to 50% of earned wages in under a minute, no paperwork.' },
  { icon: Gauge, title: 'Career Credit Score™', desc: 'A 300–900 score built from employment stability, growth, and repayment behavior.' },
  { icon: ShieldCheck, title: 'Fraud & risk engine', desc: 'ML-driven eligibility and fraud detection with full SHAP explainability.' },
  { icon: PiggyBank, title: 'Financial wellness', desc: 'Debt-to-income, savings ratio, and EMI burden — with actionable guidance.' },
  { icon: Wallet, title: 'Flexible loan products', desc: 'Salary advances, emergency loans, and education financing in one place.' },
  { icon: BarChart3, title: 'Employer analytics', desc: 'Department-level wellness, default risk, and payroll sync — in real time.' },
]

export default function Features() {
  return (
    <section className="py-24">
      <div className="container">
        <ScrollReveal className="mx-auto max-w-2xl text-center">
          <span className="text-xs font-medium uppercase tracking-widest text-primary">Platform</span>
          <h2 className="mt-3 font-display text-3xl font-semibold tracking-tight sm:text-4xl">
            Everything payroll-linked lending needs
          </h2>
          <p className="mt-3 text-muted-foreground">
            Built for finance teams who need speed, and employees who need trust.
          </p>
        </ScrollReveal>

        <div className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f, idx) => (
            <ScrollReveal key={f.title} delay={(idx % 3) * 0.08}>
              <Card className="h-full transition-transform hover:-translate-y-1">
                <CardContent className="p-6">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-aurora">
                    <f.icon className="h-5 w-5 text-white" />
                  </div>
                  <h3 className="mt-4 font-display text-base font-semibold">{f.title}</h3>
                  <p className="mt-1.5 text-sm text-muted-foreground">{f.desc}</p>
                </CardContent>
              </Card>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  )
}
