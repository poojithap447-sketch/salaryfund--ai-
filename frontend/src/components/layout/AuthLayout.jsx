import { Outlet, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles, ShieldCheck, TrendingUp, Zap } from 'lucide-react'

const FEATURES = [
  { icon: Zap, text: 'Access up to 50% of earned salary, instantly' },
  { icon: ShieldCheck, text: 'Bank-grade encryption on every transaction' },
  { icon: TrendingUp, text: 'AI-scored Career Credit, built as you grow' },
]

export default function AuthLayout() {
  return (
    <div className="grid min-h-screen grid-cols-1 bg-background lg:grid-cols-2">
      <div className="relative hidden flex-col justify-between overflow-hidden bg-mesh p-12 lg:flex">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/10" />
        <Link to="/" className="relative z-10 flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-aurora">
            <Sparkles className="h-4.5 w-4.5 h-5 w-5 text-white" />
          </div>
          <span className="font-display text-lg font-semibold">SalaryFund AI</span>
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="relative z-10 max-w-md"
        >
          <h2 className="font-display text-4xl font-semibold leading-tight tracking-tight">
            Your salary, <span className="text-gradient">available on your terms.</span>
          </h2>
          <p className="mt-4 text-muted-foreground">
            Earned-wage access, career credit intelligence, and financial wellness — built for the modern workforce.
          </p>

          <div className="mt-10 space-y-4">
            {FEATURES.map((f, i) => (
              <motion.div
                key={f.text}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.15 * i + 0.2 }}
                className="flex items-center gap-3"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg glass">
                  <f.icon className="h-4 w-4 text-primary" />
                </div>
                <span className="text-sm text-foreground/90">{f.text}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <p className="relative z-10 text-xs text-muted-foreground">© 2026 SalaryFund AI. All rights reserved.</p>
      </div>

      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-sm">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
