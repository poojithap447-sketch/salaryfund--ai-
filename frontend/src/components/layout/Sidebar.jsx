import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ChevronsLeft, Sparkles } from 'lucide-react'
import { cn } from '@/utils/cn'
import { useUIStore } from '@/store/useUIStore'
import { NAV_CONFIG } from '@/constants/navigation'
import { useAuthStore } from '@/store/useAuthStore'
import { ROLES } from '@/constants'

export default function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, mobileSidebarOpen, setMobileSidebarOpen } = useUIStore()
  const role = useAuthStore((s) => s.user?.role) || ROLES.EMPLOYEE
  const navItems = NAV_CONFIG[role] || NAV_CONFIG[ROLES.EMPLOYEE]

  return (
    <>
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}
      <motion.aside
        animate={{ width: sidebarCollapsed ? 80 : 264 }}
        transition={{ type: 'spring', stiffness: 260, damping: 28 }}
        className={cn(
          'fixed lg:sticky top-0 z-50 flex h-screen shrink-0 flex-col border-r border-border bg-surface/80 backdrop-blur-xl',
          'transition-transform lg:translate-x-0',
          mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-16 items-center gap-2 px-5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-aurora">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          {!sidebarCollapsed && (
            <span className="font-display text-sm font-semibold tracking-tight">SalaryFund AI</span>
          )}
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setMobileSidebarOpen(false)}
              className={({ isActive }) =>
                cn(
                  'group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors focus-ring',
                  isActive
                    ? 'bg-primary/15 text-primary'
                    : 'text-muted-foreground hover:bg-secondary/60 hover:text-foreground'
                )
              }
            >
              <item.icon className="h-4.5 w-4.5 h-5 w-5 shrink-0" />
              {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        <button
          onClick={toggleSidebar}
          className="hidden lg:flex items-center gap-2 border-t border-border px-5 py-4 text-xs text-muted-foreground hover:text-foreground focus-ring"
        >
          <ChevronsLeft className={cn('h-4 w-4 transition-transform', sidebarCollapsed && 'rotate-180')} />
          {!sidebarCollapsed && 'Collapse'}
        </button>
      </motion.aside>
    </>
  )
}
