import { Menu, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import Breadcrumb from './Breadcrumb'
import NotificationPanel from '@/components/common/NotificationPanel'
import ProfileMenu from '@/components/common/ProfileMenu'
import ThemeToggle from '@/components/common/ThemeToggle'
import { useUIStore } from '@/store/useUIStore'

export default function Topbar() {
  const setMobileSidebarOpen = useUIStore((s) => s.setMobileSidebarOpen)

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between gap-4 border-b border-border bg-background/70 px-4 backdrop-blur-xl sm:px-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setMobileSidebarOpen(true)}>
          <Menu className="h-5 w-5" />
        </Button>
        <div className="hidden md:block">
          <Breadcrumb />
        </div>
      </div>

      <div className="hidden max-w-sm flex-1 items-center gap-2 md:flex">
        <div className="relative w-full">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="Search loans, employees, reports…" className="pl-9" />
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <ThemeToggle className="hidden sm:flex" />
        <NotificationPanel />
        <ProfileMenu />
      </div>
    </header>
  )
}
