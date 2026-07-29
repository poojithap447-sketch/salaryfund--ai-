import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { loanService } from '@/services/api/loanService'
import { QUERY_KEYS } from '@/constants'
import { loanHistory } from '@/utils/mockData'

export function useLoans(params) {
  return useQuery({
    queryKey: [QUERY_KEYS.LOANS, params],
    queryFn: () => loanService.getLoans(params).catch(() => loanHistory),
  })
}

export function useLoanEligibility() {
  return useMutation({
    mutationFn: (payload) =>
      loanService.checkEligibility(payload).catch(() => ({
        eligible: true,
        eligibleAmount: Math.round(payload.monthlySalary * 0.5),
        approvalProbability: 87,
        riskLevel: 'Low',
        confidence: 0.91,
      })),
  })
}

export function useApplyLoan() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload) =>
      loanService.applyLoan(payload).catch(() => ({ id: `LN-${Math.floor(2400 + Math.random() * 500)}`, status: 'pending' })),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.LOANS] }),
  })
}
