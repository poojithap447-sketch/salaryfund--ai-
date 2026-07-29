import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { notificationService } from '@/services/api/notificationService'
import { QUERY_KEYS } from '@/constants'
import { recentNotifications } from '@/utils/mockData'
import { useNotificationStore } from '@/store/useNotificationStore'

export function useNotifications() {
  const setNotifications = useNotificationStore((s) => s.setNotifications)
  const query = useQuery({
    queryKey: [QUERY_KEYS.NOTIFICATIONS],
    queryFn: () => notificationService.getNotifications().catch(() => recentNotifications),
  })

  useEffect(() => {
    if (query.data) setNotifications(query.data)
  }, [query.data, setNotifications])

  return query
}
