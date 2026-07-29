import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'
import { Card, CardContent } from '@/components/ui/card'

export default function StatCard({ label, value, icon: Icon, trend, trendLabel, accent = 'primary', className }) {
  const isPositive = trend > 0
  const isNegative = trend < 0

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <Card className={cn('relative overflow-hidden', className)}>
        <div
          className={cn(
            'pointer-events-none absolute -right-6 -top-6 h-28 w-28 rounded-full blur-3xl opacity-20',
            accent === 'primary' && 'bg-primary',
            accent === 'accent' && 'bg-accent',
            accent === 'success' && 'bg-success',
            accent === 'warning' && 'bg-warning'
          )}
        />
        <CardContent className="p-5">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground">{label}</p>
              <p className="mt-2 font-display text-2xl font-semibold tracking-tight">{value}</p>
            </div>
            {Icon && (
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-secondary/70">
                <Icon className="h-4.5 w-4.5 h-5 w-5 text-primary" />
              </div>
            )}
          </div>
          {trend !== undefined && (
            <p
              className={cn(
                'mt-3 text-xs font-medium',
                isPositive && 'text-success',
                isNegative && 'text-danger',
                !isPositive && !isNegative && 'text-muted-foreground'
              )}
            >
              {isPositive ? '↑' : isNegative ? '↓' : '–'} {Math.abs(trend)}% {trendLabel}
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}
