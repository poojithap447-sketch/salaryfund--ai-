import { CheckCheck } from 'lucide-react'
import PageHeader from '@/components/common/PageHeader'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import EmptyState from '@/components/common/EmptyState'
import { useNotifications } from '@/hooks/useNotifications'
import { useNotificationStore } from '@/store/useNotificationStore'
import { cn } from '@/utils/cn'

export default function Notifications() {
  useNotifications()
  const { notifications, markAllRead, markAsRead, unreadCount } = useNotificationStore()

  return (
    <div>
      <PageHeader
        title="Notifications"
        description="Stay on top of EMI due dates, approvals, and score updates."
        actions={
          unreadCount > 0 && (
            <Button variant="outline" onClick={markAllRead}>
              <CheckCheck className="h-4 w-4" /> Mark all read
            </Button>
          )
        }
      />

      {notifications.length === 0 ? (
        <EmptyState title="No notifications" description="You're all caught up for now." />
      ) : (
        <div className="space-y-3">
          {notifications.map((n) => (
            <Card
              key={n.id}
              onClick={() => markAsRead(n.id)}
              className={cn('cursor-pointer transition-colors hover:border-primary/40', !n.read && 'border-primary/30')}
            >
              <CardContent className="flex items-start justify-between gap-4 p-5">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-medium">{n.title}</p>
                    {!n.read && <Badge>New</Badge>}
                  </div>
                  <p className="mt-1 text-sm text-muted-foreground">{n.body}</p>
                </div>
                <span className="shrink-0 text-xs text-muted-foreground">{n.time}</span>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
