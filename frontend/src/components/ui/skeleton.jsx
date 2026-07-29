import { cn } from '@/utils/cn'

function Skeleton({ className, ...props }) {
  return <div className={cn('skeleton', className)} {...props} />
}

export { Skeleton }
