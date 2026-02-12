// TanStack Query composable for task categories
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { taskCategoryService } from '@/services/taskCategory.service'
import type { TaskCategoryCreate, TaskCategoryUpdate } from '@/types/field'

/**
 * Query hook for fetching task categories with automatic caching
 */
export function useTaskCategories(workspaceId: number, includeInactive = false) {
  return useQuery({
    queryKey: ['task-categories', workspaceId, includeInactive],
    queryFn: () => taskCategoryService.getCategories(workspaceId, includeInactive),
    staleTime: 5 * 60 * 1000, // 5 minutes cache
    enabled: !!workspaceId,
  })
}

/**
 * Mutation hook for creating a task category
 */
export function useCreateTaskCategory() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: TaskCategoryCreate) =>
      taskCategoryService.createCategory(data),
    onSuccess: (_, variables) => {
      // Invalidate the categories list for this workspace
      queryClient.invalidateQueries({
        queryKey: ['task-categories', variables.workspace_id]
      })
    },
  })
}

/**
 * Mutation hook for updating a task category
 */
export function useUpdateTaskCategory() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TaskCategoryUpdate }) =>
      taskCategoryService.updateCategory(id, data),
    onSuccess: (data) => {
      // Invalidate the categories list for this workspace
      queryClient.invalidateQueries({
        queryKey: ['task-categories', data.workspace_id]
      })
    },
  })
}

/**
 * Mutation hook for deleting a task category
 */
export function useDeleteTaskCategory() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id }: { id: number; workspaceId: number }) =>
      taskCategoryService.deleteCategory(id),
    onSuccess: (_, variables) => {
      // Invalidate the categories list
      queryClient.invalidateQueries({
        queryKey: ['task-categories', variables.workspaceId]
      })
    },
  })
}
