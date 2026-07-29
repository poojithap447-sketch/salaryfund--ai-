import { useNavigate } from 'react-router-dom'
import { Check } from 'lucide-react'
import PublicNavbar from '@/components/layout/PublicNavbar'
import Footer from '@/components/layout/Footer'
import ScrollReveal from '@/components/animations/ScrollReveal'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { cn } from '@/utils/cn'
import { ROUTES } from '@/constants'

const PLANS = [
  {
    name: 'Starter',
    price: '₹0',
    period: 'per employee / mo',
    desc: 'For teams piloting earned-wage access.',
    features: ['Up to 100 employees', 'Salary advance only', 'Standard risk engine', 'Email support'],
  },
  {
    name: 'Growth',
    price: '₹29',
    period: 'per employee / mo',
    desc: 'For scaling companies with active lending needs.',
    features: ['Up to 5,000 employees', 'All loan types', 'Career Credit Score™', 'Fraud detection', 'Priority support'],
    featured: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: 'volume pricing',
    desc: 'For large organizations and lender networks.',
    features: ['Unlimited employees', 'Custom risk models', 'Dedicated account manager', 'SLA-backed uptime', 'SSO & audit logs'],
  },
]

export default function Pricing() {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-background">
      <PublicNavbar />

      <section className="bg-mesh py-24">
        <div className="container">
          <ScrollReveal className="mx-auto max-w-2xl text-center">
            <span className="text-xs font-medium uppercase tracking-widest text-primary">Pricing</span>
            <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight">Simple, per-employee pricing</h1>
            <p className="mt-4 text-muted-foreground">No setup fees. No lock-in. Scale as your team grows.</p>
          </ScrollReveal>

          <div className="mx-auto mt-14 grid max-w-5xl grid-cols-1 gap-6 lg:grid-cols-3">
            {PLANS.map((plan, idx) => (
              <ScrollReveal key={plan.name} delay={idx * 0.1}>
                <Card className={cn('relative h-full', plan.featured && 'border-primary/50 shadow-lg shadow-primary/10')}>
                  {plan.featured && (
                    <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-aurora px-3 py-1 text-xs font-medium text-white">
                      Most popular
                    </span>
                  )}
                  <CardHeader>
                    <CardTitle>{plan.name}</CardTitle>
                    <CardDescription>{plan.desc}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-6">
                      <span className="font-display text-3xl font-semibold">{plan.price}</span>
                      <span className="ml-1.5 text-sm text-muted-foreground">{plan.period}</span>
                    </div>
                    <ul className="space-y-2.5">
                      {plan.features.map((f) => (
                        <li key={f} className="flex items-start gap-2 text-sm">
                          <Check className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                          {f}
                        </li>
                      ))}
                    </ul>
                    <Button
                      variant={plan.featured ? 'aurora' : 'outline'}
                      className="mt-8 w-full"
                      onClick={() => navigate(ROUTES.REGISTER)}
                    >
                      Get started
                    </Button>
                  </CardContent>
                </Card>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
