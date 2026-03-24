// TanStack Query composable for customers
import { useQuery } from '@tanstack/vue-query'
import { customerService } from '@/services/customer.service'

/**
 * Query hook for fetching companies with automatic caching
 */
export function useCompanies() {
  return useQuery({
    queryKey: ['companies'],
    queryFn: () => customerService.getCompanies(),
    staleTime: 10 * 60 * 1000, // 10 minutes cache
  })
}

/**
 * Query hook for fetching full company records used for licence analytics
 */
export function useAllCompanies() {
  return useQuery({
    queryKey: ['all-companies'],
    queryFn: () => customerService.getAllCompanies(),
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  })
}

/**
 * Query hook for fetching licences with automatic caching
 */
export function useLicences() {
  return useQuery({
    queryKey: ['licences'],
    queryFn: () => customerService.getLicences(),
    staleTime: 2 * 60 * 1000, // 2 minutes cache
  })
}
