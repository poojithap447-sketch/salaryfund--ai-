import ScrollReveal from '@/components/animations/ScrollReveal'
import AnimatedCounter from '@/components/animations/AnimatedCounter'

const STATS = [
  { value: 128400, suffix: '+', label: 'Employees onboarded' },
  { value: 64, suffix: '', label: 'Companies live' },
  { value: 8.4, prefix: '₹', suffix: 'Cr', decimals: 1, label: 'Disbursed monthly' },
  { value: 99.98, suffix: '%', decimals: 2, label: 'Platform uptime' },
]

export default function Stats() {
  return (
    <section className="border-y border-white/[0.06] bg-surface/40 py-16">
      <div className="container">
        <div className="grid grid-cols-2 gap-8 sm:grid-cols-4">
          {STATS.map((stat, idx) => (
            <ScrollReveal key={stat.label} delay={idx * 0.08} className="text-center">
              <p className="font-display text-3xl font-semibold tracking-tight sm:text-4xl">
                <AnimatedCounter value={stat.value} prefix={stat.prefix} suffix={stat.suffix} decimals={stat.decimals || 0} />
              </p>
              <p className="mt-1.5 text-sm text-muted-foreground">{stat.label}</p>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  )
}
