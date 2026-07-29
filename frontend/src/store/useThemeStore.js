import { create } from 'zustand'
import { persist } from 'zustand/middleware'

function applyTheme(theme) {
  const root = window.document.documentElement
  const isDark =
    theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
  root.classList.toggle('dark', isDark)
}

export const useThemeStore = create(
  persist(
    (set, get) => ({
      theme: 'dark', // 'light' | 'dark' | 'system'
      setTheme: (theme) => {
        applyTheme(theme)
        set({ theme })
      },
      init: () => applyTheme(get().theme),
    }),
    { name: 'salaryfund-theme' }
  )
)
