import { Inbox } from 'lucide-react'
import { cn } from '@/utils/cn'

export default function EmptyState({ icon: Icon = Inbox, title = 'Nothing here yet', description, action, className }) {
  return (
    <div className={cn('flex flex-col items-center justify-center rounded-2xl border border-dashed border-border py-14 text-center', className)}>
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-secondary/60">
        <Icon className="h-5 w-5 text-muted-foreground" />
      </div>
      <p className="mt-4 text-sm font-medium">{title}</p>
      {description && <p className="mt-1 max-w-xs text-xs text-muted-foreground">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
