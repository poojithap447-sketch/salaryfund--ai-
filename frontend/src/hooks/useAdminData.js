import { useQuery } from '@tanstack/react-query'
import { adminService } from '@/services/api/adminService'
import { QUERY_KEYS } from '@/constants'
import { adminSummary, revenueTrend, auditLogs } from '@/utils/mockData'

export function useAdminSummary() {
  return useQuery({
    queryKey: [QUERY_KEYS.ADMIN_SUMMARY],
    queryFn: () => adminService.getSummary().catch(() => adminSummary),
  })
}

export function useRevenueTrend() {
  return useQuery({
    queryKey: [QUERY_KEYS.ADMIN_SUMMARY, 'revenue'],
    queryFn: () => Promise.resolve(revenueTrend),
  })
}

export function useAuditLogs() {
  return useQuery({
    queryKey: [QUERY_KEYS.ADMIN_SUMMARY, 'audit-logs'],
    queryFn: () => adminService.getAuditLogs().catch(() => auditLogs),
  })
}
