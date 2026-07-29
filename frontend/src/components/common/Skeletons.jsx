import { Skeleton } from '@/components/ui/skeleton'
import { Card, CardContent } from '@/components/ui/card'

export function StatCardSkeleton() {
  return (
    <Card>
      <CardContent className="p-5">
        <Skeleton className="h-3 w-24" />
        <Skeleton className="mt-3 h-7 w-32" />
        <Skeleton className="mt-3 h-3 w-20" />
      </CardContent>
    </Card>
  )
}

export function ChartSkeleton({ height = 280 }) {
  return (
    <Card>
      <CardContent className="p-5">
        <Skeleton className="h-4 w-40" />
        <Skeleton className="mt-4 w-full" style={{ height }} />
      </CardContent>
    </Card>
  )
}

export function TableSkeleton({ rows = 5 }) {
  return (
    <Card>
      <CardContent className="p-5 space-y-3">
        {Array.from({ length: rows }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </CardContent>
    </Card>
  )
}
