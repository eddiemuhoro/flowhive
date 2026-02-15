// Field Activity Service
// Handles all field operations activity tracking API calls

import { apiClient } from "./api";
import type {
  FieldActivity,
  FieldActivityCreate,
  FieldActivityUpdate,
  FieldActivityDetail,
  FieldActivityFilters,
  FieldAnalytics,
} from "@/types/field";

export const fieldActivityService = {
  /**
   * Get all field activities for a workspace with optional filters
   * @param workspaceId - The workspace ID
   * @param filters - Optional filters for date, staff, category, customer
   */
  async getActivities(
    workspaceId: number,
    filters?: FieldActivityFilters,
  ): Promise<FieldActivity[]> {
    const response = await apiClient.get<FieldActivity[]>(
      `/field-activities/workspace/${workspaceId}`,
      {
        params: filters,
      },
    );
    return response.data;
  },

  /**
   * Get a single field activity with photos
   * @param activityId - The activity ID
   * @param workspaceId - The workspace ID for validation
   */
  async getActivity(
    activityId: number,
    workspaceId: number,
  ): Promise<FieldActivityDetail> {
    const response = await apiClient.get<FieldActivityDetail>(
      `/field-activities/${activityId}`,
      {
        params: { workspace_id: workspaceId },
      },
    );
    return response.data;
  },

  /**
   * Create a new field activity
   * @param data - Activity creation data
   */
  async createActivity(data: FieldActivityCreate): Promise<FieldActivity> {
    const response = await apiClient.post<FieldActivity>(
      "/field-activities",
      data,
    );
    return response.data;
  },

  /**
   * Update an existing field activity
   * @param activityId - The activity ID
   * @param workspaceId - The workspace ID for validation
   * @param data - Activity update data
   */
  async updateActivity(
    activityId: number,
    workspaceId: number,
    data: FieldActivityUpdate,
  ): Promise<FieldActivity> {
    const response = await apiClient.put<FieldActivity>(
      `/field-activities/${activityId}`,
      data,
      {
        params: { workspace_id: workspaceId },
      },
    );
    return response.data;
  },

  /**
   * Delete a field activity (only creator or manager)
   * @param activityId - The activity ID
   * @param workspaceId - The workspace ID for validation
   */
  async deleteActivity(activityId: number, workspaceId: number): Promise<void> {
    await apiClient.delete(`/field-activities/${activityId}`, {
      params: { workspace_id: workspaceId },
    });
  },

  /**
   * Get analytics for field activities (manager/executive only)
   * @param workspaceId - The workspace ID
   * @param dateFrom - Start date (YYYY-MM-DD)
   * @param dateTo - End date (YYYY-MM-DD)
   */
  async getAnalytics(
    workspaceId: number,
    dateFrom?: string,
    dateTo?: string,
  ): Promise<FieldAnalytics> {
    const response = await apiClient.get<FieldAnalytics>(
      `/field-activities/workspace/${workspaceId}/analytics`,
      {
        params: {
          date_from: dateFrom,
          date_to: dateTo,
        },
      },
    );
    return response.data;
  },

  /**
   * Get pending tasks assigned to the current user
   * @param workspaceId - The workspace ID
   */
  async getPendingTasks(workspaceId: number): Promise<FieldActivity[]> {
    const response = await apiClient.get<FieldActivity[]>(
      `/field-activities/workspace/${workspaceId}/pending`,
    );
    return response.data;
  },
  /**
   * Get count of pending tasks for current user
   * @param workspaceId - The workspace ID
   */
  async getPendingTasksCount(workspaceId: number): Promise<number> {
    const tasks = await this.getPendingTasks(workspaceId);
    return tasks.length;
  },
  /**
   * Get pending tasks created/assigned by the current user (managers/executives only)
   * @param workspaceId - The workspace ID
   */
  async getTasksAssignedByMe(workspaceId: number): Promise<FieldActivity[]> {
    const response = await apiClient.get<FieldActivity[]>(
      `/field-activities/workspace/${workspaceId}/assigned-by-me`,
    );
    return response.data;
  },

  /**
   * Upload a photo for a field activity
   * @param activityId - The activity ID
   * @param workspaceId - The workspace ID for validation
   * @param file - The image file to upload (max 10MB)
   */
  async uploadPhoto(
    activityId: number,
    workspaceId: number,
    file: File,
  ): Promise<{ message: string; photo_id: number }> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post<{
      message: string;
      photo_id: number;
    }>(`/field-activities/${activityId}/photos`, formData, {
      params: { workspace_id: workspaceId },
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  /**
   * Delete a photo from a field activity
   * @param activityId - The activity ID
   * @param photoId - The photo ID
   * @param workspaceId - The workspace ID for validation
   */
  async deletePhoto(
    activityId: number,
    photoId: number,
    workspaceId: number,
  ): Promise<void> {
    await apiClient.delete(
      `/field-activities/${activityId}/photos/${photoId}`,
      {
        params: { workspace_id: workspaceId },
      },
    );
  },
};
