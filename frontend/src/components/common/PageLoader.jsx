import { Sparkles } from 'lucide-react'

export default function PageLoader() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-3">
        <div className="flex h-10 w-10 animate-pulse-glow items-center justify-center rounded-xl bg-aurora">
          <Sparkles className="h-5 w-5 text-white" />
        </div>
        <p className="text-xs text-muted-foreground">Loading SalaryFund AI…</p>
      </div>
    </div>
  )
}
