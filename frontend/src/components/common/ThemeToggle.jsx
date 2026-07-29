import { Monitor, Moon, Sun } from 'lucide-react'
import { useThemeStore } from '@/store/useThemeStore'
import { cn } from '@/utils/cn'

const OPTIONS = [
  { value: 'light', icon: Sun },
  { value: 'dark', icon: Moon },
  { value: 'system', icon: Monitor },
]

export default function ThemeToggle({ className }) {
  const { theme, setTheme } = useThemeStore()

  return (
    <div className={cn('flex items-center gap-0.5 rounded-full border border-border bg-secondary/40 p-1', className)}>
      {OPTIONS.map(({ value, icon: Icon }) => (
        <button
          key={value}
          onClick={() => setTheme(value)}
          className={cn(
            'flex h-7 w-7 items-center justify-center rounded-full transition-colors focus-ring',
            theme === value ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground'
          )}
          aria-label={`${value} theme`}
        >
          <Icon className="h-3.5 w-3.5" />
        </button>
      ))}
    </div>
  )
}
