import { Bell, CheckCheck } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useNotifications } from '@/hooks/useNotifications'
import { useNotificationStore } from '@/store/useNotificationStore'
import { cn } from '@/utils/cn'

export default function NotificationPanel() {
  useNotifications()
  const { notifications, unreadCount, markAllRead, markAsRead } = useNotificationStore()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <span className="absolute right-1.5 top-1.5 flex h-2 w-2 rounded-full bg-danger">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-danger opacity-75" />
            </span>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80 p-0">
        <div className="flex items-center justify-between px-3 py-2.5">
          <span className="text-sm font-semibold">Notifications</span>
          {unreadCount > 0 && (
            <button onClick={markAllRead} className="flex items-center gap-1 text-xs text-primary hover:underline">
              <CheckCheck className="h-3.5 w-3.5" /> Mark all read
            </button>
          )}
        </div>
        <DropdownMenuSeparator className="mx-0" />
        <div className="max-h-80 overflow-y-auto p-1.5">
          {notifications.length === 0 && (
            <p className="px-3 py-6 text-center text-sm text-muted-foreground">You're all caught up.</p>
          )}
          {notifications.map((n) => (
            <button
              key={n.id}
              onClick={() => markAsRead(n.id)}
              className={cn(
                'flex w-full flex-col items-start gap-0.5 rounded-lg px-3 py-2.5 text-left transition-colors hover:bg-secondary/60',
                !n.read && 'bg-primary/5'
              )}
            >
              <div className="flex w-full items-center justify-between gap-2">
                <span className="text-sm font-medium">{n.title}</span>
                {!n.read && <Badge className="shrink-0">New</Badge>}
              </div>
              <span className="text-xs text-muted-foreground">{n.body}</span>
              <span className="text-[11px] text-muted-foreground/70">{n.time}</span>
            </button>
          ))}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
