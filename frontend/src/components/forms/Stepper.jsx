import { Check } from 'lucide-react'
import { cn } from '@/utils/cn'

export default function Stepper({ steps, currentStep }) {
  return (
    <div className="flex items-center">
      {steps.map((step, idx) => {
        const isCompleted = idx < currentStep
        const isActive = idx === currentStep
        return (
          <div key={step} className="flex flex-1 items-center last:flex-none">
            <div className="flex flex-col items-center gap-1.5">
              <div
                className={cn(
                  'flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold transition-colors',
                  isCompleted && 'border-primary bg-primary text-primary-foreground',
                  isActive && 'border-primary text-primary',
                  !isCompleted && !isActive && 'border-border text-muted-foreground'
                )}
              >
                {isCompleted ? <Check className="h-4 w-4" /> : idx + 1}
              </div>
              <span
                className={cn(
                  'hidden text-[11px] font-medium sm:block',
                  isActive ? 'text-foreground' : 'text-muted-foreground'
                )}
              >
                {step}
              </span>
            </div>
            {idx < steps.length - 1 && (
              <div className={cn('mx-2 h-0.5 flex-1 rounded-full transition-colors', isCompleted ? 'bg-primary' : 'bg-border')} />
            )}
          </div>
        )
      })}
    </div>
  )
}
