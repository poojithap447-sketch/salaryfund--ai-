import { createContext, useContext, useMemo } from 'react'

const AppConfigContext = createContext(null)

export function AppConfigProvider({ children }) {
  const config = useMemo(
    () => ({
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      appName: import.meta.env.VITE_APP_NAME || 'SalaryFund AI',
      enableLenderPortal: import.meta.env.VITE_ENABLE_LENDER_PORTAL !== 'false',
      enableAdminPortal: import.meta.env.VITE_ENABLE_ADMIN_PORTAL !== 'false',
    }),
    []
  )

  return <AppConfigContext.Provider value={config}>{children}</AppConfigContext.Provider>
}

export function useAppConfig() {
  const ctx = useContext(AppConfigContext)
  if (!ctx) throw new Error('useAppConfig must be used within AppConfigProvider')
  return ctx
}
