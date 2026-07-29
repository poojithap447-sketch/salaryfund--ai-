import { useNavigate } from 'react-router-dom'
import { ArrowRight, ShieldCheck, TrendingUp, Wallet } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import HeroAnimation from '@/components/animations/HeroAnimation'
import { ROUTES } from '@/constants'

export default function Hero() {
  const navigate = useNavigate()
  const title = 'Earn today, not on the 1st.'

  return (
    <section className="relative overflow-hidden bg-mesh pb-24 pt-20 sm:pt-28">
      <div
        data-hero-orb
        className="pointer-events-none absolute left-[8%] top-24 h-64 w-64 rounded-full bg-primary/25 blur-[100px]"
      />
      <div
        data-hero-orb
        className="pointer-events-none absolute right-[10%] top-40 h-72 w-72 rounded-full bg-accent/20 blur-[110px]"
      />

      <HeroAnimation>
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <span
              data-hero-eyebrow
              className="inline-flex items-center gap-2 rounded-full border border-border bg-secondary/50 px-3 py-1 text-xs font-medium text-muted-foreground"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              Now live for 64 companies across India
            </span>

            <h1 data-hero-title className="mt-6 font-display text-4xl font-semibold leading-[1.1] tracking-tight sm:text-6xl">
              {title.split(' ').map((word, i) => (
                <span key={i} className="mr-3 inline-block last:mr-0">
                  {word === 'today,' ? <span className="text-gradient">{word}</span> : word}
                </span>
              ))}
            </h1>

            <p data-hero-sub className="mx-auto mt-6 max-w-xl text-base text-muted-foreground sm:text-lg">
              SalaryFund AI gives your workforce instant access to earned wages, an AI-scored Career Credit, and
              real financial wellness — all wired straight into payroll.
            </p>

            <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Button data-hero-cta variant="aurora" size="lg" onClick={() => navigate(ROUTES.REGISTER)}>
                Get started free <ArrowRight className="h-4 w-4" />
              </Button>
              <Button data-hero-cta variant="outline" size="lg" onClick={() => navigate(ROUTES.PRICING)}>
                View pricing
              </Button>
            </div>
          </div>

          <div data-hero-panel className="mx-auto mt-16 max-w-4xl">
            <Card className="card-shadow">
              <CardContent className="grid grid-cols-1 gap-4 p-6 sm:grid-cols-3">
                {[
                  { icon: Wallet, label: 'Available now', value: '₹64,000', tone: 'text-primary' },
                  { icon: TrendingUp, label: 'Career Credit Score™', value: '742', tone: 'text-accent' },
                  { icon: ShieldCheck, label: 'Financial wellness', value: '78 / 100', tone: 'text-success' },
                ].map((item) => (
                  <div key={item.label} className="flex items-center gap-3 rounded-xl bg-secondary/40 p-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-background/60">
                      <item.icon className={`h-4.5 w-4.5 h-5 w-5 ${item.tone}`} />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">{item.label}</p>
                      <p className="font-display text-lg font-semibold">{item.value}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </HeroAnimation>
    </section>
  )
}
