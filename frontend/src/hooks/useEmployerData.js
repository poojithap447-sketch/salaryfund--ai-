import { useQuery } from '@tanstack/react-query'
import { employerService } from '@/services/api/employerService'
import { QUERY_KEYS } from '@/constants'
import { employerSummary, departmentAnalytics, loanTypeSplit } from '@/utils/mockData'

export function useEmployerSummary() {
  return useQuery({
    queryKey: [QUERY_KEYS.EMPLOYER_SUMMARY],
    queryFn: () => employerService.getSummary().catch(() => employerSummary),
  })
}

export function useDepartmentAnalytics() {
  return useQuery({
    queryKey: [QUERY_KEYS.EMPLOYER_SUMMARY, 'departments'],
    queryFn: () => employerService.getDepartmentAnalytics().catch(() => departmentAnalytics),
  })
}

export function useLoanTypeSplit() {
  return useQuery({
    queryKey: [QUERY_KEYS.EMPLOYER_SUMMARY, 'loan-split'],
    queryFn: () => Promise.resolve(loanTypeSplit),
  })
}
