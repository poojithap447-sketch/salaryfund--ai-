import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/store/useAuthStore'
import { ROUTES } from '@/constants'

export default function ProtectedRoute({ allowedRoles }) {
  const { isAuthenticated, user } = useAuthStore()

  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} replace />

  if (allowedRoles && user?.role && !allowedRoles.includes(user.role)) {
    return <Navigate to={ROUTES.HOME} replace />
  }

  return <Outlet />
}
