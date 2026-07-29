import { Link } from 'react-router-dom'
import { Compass } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ROUTES } from '@/constants'

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background bg-mesh p-8 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
        <Compass className="h-7 w-7 text-primary" />
      </div>
      <h1 className="font-display text-5xl font-semibold tracking-tight">404</h1>
      <p className="max-w-sm text-muted-foreground">This page drifted off the map. Let's get you back on track.</p>
      <Button asChild variant="aurora" size="lg">
        <Link to={ROUTES.HOME}>Back to home</Link>
      </Button>
    </div>
  )
}
