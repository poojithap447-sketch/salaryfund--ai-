import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import AnimatedCounter from '@/components/animations/AnimatedCounter'

export default function CareerScoreGauge({ score = 742, min = 300, max = 900, riskLevel = 'Low' }) {
  const pct = Math.min(100, Math.max(0, ((score - min) / (max - min)) * 100))
  const radius = 70
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (pct / 100) * circumference

  return (
    <Card>
      <CardHeader>
        <CardTitle>Career Credit Score™</CardTitle>
        <CardDescription>Your standing based on stability, growth, and repayment behavior</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        <div className="relative flex h-44 w-44 items-center justify-center">
          <svg width="176" height="176" viewBox="0 0 176 176" className="-rotate-90">
            <circle cx="88" cy="88" r={radius} fill="none" stroke="hsl(var(--secondary))" strokeWidth="14" />
            <motion.circle
              cx="88"
              cy="88"
              r={radius}
              fill="none"
              stroke="url(#scoreGradient)"
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            <defs>
              <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="hsl(258 90% 66%)" />
                <stop offset="100%" stopColor="hsl(199 89% 58%)" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute flex flex-col items-center">
            <span className="font-display text-3xl font-semibold">
              <AnimatedCounter value={score} />
            </span>
            <span className="text-xs text-muted-foreground">of {max}</span>
          </div>
        </div>

        <Badge variant="success" className="mt-4">
          {riskLevel} risk
        </Badge>

        <div className="mt-5 flex w-full justify-between text-xs text-muted-foreground">
          <span>{min}</span>
          <span>{max}</span>
        </div>
      </CardContent>
    </Card>
  )
}
