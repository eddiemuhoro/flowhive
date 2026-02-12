// TanStack Query composable for field activities
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { computed, unref, type MaybeRef } from 'vue'
import { fieldActivityService } from '@/services/fieldActivity.service'
import type { FieldActivityCreate, FieldActivityUpdate } from '@/types/field'

/**
 * Query hook for fetching field activities with automatic caching
 */
export function useFieldActivities(
  workspaceId: MaybeRef<number>,
  filters?: MaybeRef<{
    dateFrom?: string
    dateTo?: string
    supportStaffId?: number
    taskCategoryId?: number
    customerName?: string
    search?: string
  }>
) {
  const queryKey = computed(() => ['field-activities', unref(workspaceId), unref(filters)])

  return useQuery({
    queryKey,
    queryFn: () => fieldActivityService.getActivities(unref(workspaceId), unref(filters)),
    staleTime: 2 * 60 * 1000, // 2 minutes cache
    enabled: computed(() => !!unref(workspaceId)),
  })
}

/**
 * Query hook for fetching a single field activity
 */
export function useFieldActivity(activityId: number, workspaceId: number) {
  return useQuery({
    queryKey: ['field-activity', activityId],
    queryFn: () => fieldActivityService.getActivity(activityId, workspaceId),
    staleTime: 5 * 60 * 1000, // 5 minutes cache
    enabled: !!activityId && !!workspaceId,
  })
}

/**
 * Mutation hook for creating a field activity
 */
export function useCreateFieldActivity() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: FieldActivityCreate) =>
      fieldActivityService.createActivity(data),
    onSuccess: (_, variables) => {
      // Invalidate the activities list for this workspace
      queryClient.invalidateQueries({
        queryKey: ['field-activities', variables.workspace_id]
      })
    },
  })
}

/**
 * Mutation hook for updating a field activity
 */
export function useUpdateFieldActivity() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, workspaceId, data }: {
      id: number
      workspaceId: number
      data: FieldActivityUpdate
    }) => fieldActivityService.updateActivity(id, workspaceId, data),
    onSuccess: (_, variables) => {
      // Invalidate both the single activity and the list
      queryClient.invalidateQueries({
        queryKey: ['field-activity', variables.id]
      })
      queryClient.invalidateQueries({
        queryKey: ['field-activities', variables.workspaceId]
      })
    },
  })
}

/**
 * Mutation hook for deleting a field activity
 */
export function useDeleteFieldActivity() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, workspaceId }: { id: number; workspaceId: number }) =>
      fieldActivityService.deleteActivity(id, workspaceId),
    onSuccess: (_, variables) => {
      // Invalidate the activities list
      queryClient.invalidateQueries({
        queryKey: ['field-activities', variables.workspaceId]
      })
    },
  })
}

/**
 * Mutation hook for uploading photos to a field activity
 */
export function useUploadActivityPhoto() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ activityId, workspaceId, file }: {
      activityId: number
      workspaceId: number
      file: File
    }) => fieldActivityService.uploadPhoto(activityId, workspaceId, file),
    onSuccess: (_, variables) => {
      // Invalidate the activity to refresh with new photos
      queryClient.invalidateQueries({
        queryKey: ['field-activity', variables.activityId]
      })
    },
  })
}

/**
 * Mutation hook for deleting a photo from a field activity
 */
export function useDeleteActivityPhoto() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ activityId, photoId, workspaceId }: {
      activityId: number
      photoId: number
      workspaceId: number
    }) => fieldActivityService.deletePhoto(activityId, photoId, workspaceId),
    onSuccess: (_, variables) => {
      // Invalidate the activity to refresh without the deleted photo
      queryClient.invalidateQueries({
        queryKey: ['field-activity', variables.activityId]
      })
    },
  })
}
