import { Link, useLocation } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'

export default function Breadcrumb() {
  const { pathname } = useLocation()
  const segments = pathname.split('/').filter(Boolean)

  if (segments.length === 0) return null

  return (
    <nav className="flex items-center gap-1.5 text-sm text-muted-foreground">
      <Link to="/" className="hover:text-foreground transition-colors">
        Home
      </Link>
      {segments.map((seg, idx) => {
        const path = '/' + segments.slice(0, idx + 1).join('/')
        const label = seg.replace(/-/g, ' ')
        const isLast = idx === segments.length - 1
        return (
          <span key={path} className="flex items-center gap-1.5">
            <ChevronRight className="h-3.5 w-3.5" />
            {isLast ? (
              <span className="capitalize text-foreground font-medium">{label}</span>
            ) : (
              <Link to={path} className="capitalize hover:text-foreground transition-colors">
                {label}
              </Link>
            )}
          </span>
        )
      })}
    </nav>
  )
}
