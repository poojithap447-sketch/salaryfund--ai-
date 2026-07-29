import * as React from 'react'
import { cn } from '@/utils/cn'

const Input = React.forwardRef(({ className, type = 'text', ...props }, ref) => (
  <input
    type={type}
    ref={ref}
    className={cn(
      'flex h-11 w-full rounded-xl border border-input bg-surface/60 px-4 py-2 text-sm transition-colors',
      'placeholder:text-muted-foreground focus-ring',
      'file:border-0 file:bg-transparent file:text-sm file:font-medium',
      'disabled:cursor-not-allowed disabled:opacity-50',
      className
    )}
    {...props}
  />
))
Input.displayName = 'Input'

export { Input }
