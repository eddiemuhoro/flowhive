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
