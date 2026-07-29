import { useEffect } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '@/services/queryClient'
import { Toaster } from '@/components/ui/toaster'
import ErrorBoundary from '@/components/common/ErrorBoundary'
import { useThemeStore } from '@/store/useThemeStore'
import { AppConfigProvider } from '@/context/AppConfigContext'
import AppRoutes from '@/routes/AppRoutes'

export default function App() {
  const init = useThemeStore((s) => s.init)

  useEffect(() => {
    init()
  }, [init])

  return (
    <ErrorBoundary>
      <AppConfigProvider>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppRoutes />
            <Toaster />
          </BrowserRouter>
        </QueryClientProvider>
      </AppConfigProvider>
    </ErrorBoundary>
  )
}
