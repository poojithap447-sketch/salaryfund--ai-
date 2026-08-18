import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Menu, Sparkles, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ROUTES } from '@/constants'

const LINKS = [
  { label: 'About', path: ROUTES.ABOUT },
]

export default function PublicNavbar() {
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 border-b border-white/[0.06] bg-background/70 backdrop-blur-xl">
      <div className="container flex h-16 items-center justify-between">
        <Link to={ROUTES.HOME} className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-aurora">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <span className="font-display text-sm font-semibold tracking-tight">SalaryFund AI</span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {LINKS.map((l) => (
            <Link key={l.path} to={l.path} className="text-sm text-muted-foreground transition-colors hover:text-foreground">
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <Button variant="ghost" onClick={() => navigate(ROUTES.LOGIN)}>
            Sign in
          </Button>
          <Button variant="aurora" onClick={() => navigate(ROUTES.REGISTER)}>
            Get started
          </Button>
        </div>

        <button className="md:hidden" onClick={() => setOpen((o) => !o)}>
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {open && (
        <div className="border-t border-border px-4 py-4 md:hidden">
          {LINKS.map((l) => (
            <Link key={l.path} to={l.path} onClick={() => setOpen(false)} className="block py-2 text-sm text-muted-foreground">
              {l.label}
            </Link>
          ))}
          <div className="mt-3 flex gap-2">
            <Button variant="outline" className="flex-1" onClick={() => navigate(ROUTES.LOGIN)}>
              Sign in
            </Button>
            <Button variant="aurora" className="flex-1" onClick={() => navigate(ROUTES.REGISTER)}>
              Get started
            </Button>
          </div>
        </div>
      )}
    </header>
  )
}
