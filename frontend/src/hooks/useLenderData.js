import { useQuery } from '@tanstack/react-query'
import { lenderService } from '@/services/api/lenderService'
import { QUERY_KEYS } from '@/constants'
import { lenderSummary, riskDistribution } from '@/utils/mockData'

export function useLenderSummary() {
  return useQuery({
    queryKey: [QUERY_KEYS.LENDER_SUMMARY],
    queryFn: () => lenderService.getSummary().catch(() => lenderSummary),
  })
}

export function useRiskDistribution() {
  return useQuery({
    queryKey: [QUERY_KEYS.LENDER_SUMMARY, 'risk'],
    queryFn: () => Promise.resolve(riskDistribution),
  })
}
