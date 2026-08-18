import { Link } from 'react-router-dom'
import { Sparkles } from 'lucide-react'
import { ROUTES } from '@/constants'

export default function Footer() {
  return (
    <footer className="border-t border-white/[0.06] py-12">
      <div className="container flex flex-col items-center justify-between gap-6 sm:flex-row">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-aurora">
            <Sparkles className="h-3.5 w-3.5 text-white" />
          </div>
          <span className="font-display text-sm font-semibold">SalaryFund AI</span>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
          <Link to={ROUTES.ABOUT} className="hover:text-foreground">About</Link>
          <Link to={ROUTES.SUPPORT} className="hover:text-foreground">Support</Link>
          <a href="#" className="hover:text-foreground">Privacy</a>
          <a href="#" className="hover:text-foreground">Terms</a>
        </div>
        <p className="text-xs text-muted-foreground">© 2026 SalaryFund AI, Inc.</p>
      </div>
    </footer>
  )
}
