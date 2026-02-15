// Field Activity Store
// Manages field operations activities with filtering and analytics

import { defineStore } from "pinia";
import { fieldActivityService } from "@/services/fieldActivity.service";
import type {
  FieldActivity,
  FieldActivityCreate,
  FieldActivityUpdate,
  FieldActivityDetail,
  FieldActivityFilters,
  FieldAnalytics,
} from "@/types/field";

interface FieldActivityState {
  activities: FieldActivity[];
  currentActivity: FieldActivityDetail | null;
  analytics: FieldAnalytics | null;
  loading: boolean;
  error: string | null;
  filters: FieldActivityFilters;
  currentWorkspaceId: number | null;
}

export const useFieldActivityStore = defineStore("fieldActivity", {
  state: (): FieldActivityState => ({
    activities: [],
    currentActivity: null,
    analytics: null,
    loading: false,
    error: null,
    filters: {},
    currentWorkspaceId: null,
  }),

  getters: {
    /**
     * Get activities sorted by date (newest first)
     */
    sortedActivities: (state): FieldActivity[] => {
      return [...state.activities].sort((a, b) => {
        const dateA = new Date(`${a.activity_date} ${a.start_time}`);
        const dateB = new Date(`${b.activity_date} ${b.start_time}`);
        return dateB.getTime() - dateA.getTime();
      });
    },

    /**
     * Get total hours across all activities
     */
    totalHours: (state): number => {
      return state.activities.reduce(
        (sum, activity) => sum + (activity.duration_hours || 0),
        0,
      );
    },

    /**
     * Get activities grouped by date
     */
    activitiesByDate: (state): Record<string, FieldActivity[]> => {
      const grouped: Record<string, FieldActivity[]> = {};
      state.activities.forEach((activity) => {
        if (!grouped[activity.activity_date]) {
          grouped[activity.activity_date] = [];
        }
        grouped[activity.activity_date].push(activity);
      });
      return grouped;
    },

    /**
     * Check if filters are active
     */
    hasActiveFilters: (state): boolean => {
      return Object.keys(state.filters).length > 0;
    },
  },

  actions: {
    /**
     * Fetch all activities for a workspace with optional filters
     */
    async fetchActivities(workspaceId: number, filters?: FieldActivityFilters) {
      this.loading = true;
      this.error = null;
      this.currentWorkspaceId = workspaceId;
      if (filters) {
        this.filters = filters;
      }

      try {
        this.activities = await fieldActivityService.getActivities(
          workspaceId,
          this.filters,
        );
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to fetch activities";
        console.error("Error fetching activities:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch a single activity with photos
     */
    async fetchActivity(activityId: number, workspaceId: number) {
      this.loading = true;
      this.error = null;

      try {
        this.currentActivity = await fieldActivityService.getActivity(
          activityId,
          workspaceId,
        );
      } catch (error: any) {
        this.error = error.response?.data?.detail || "Failed to fetch activity";
        console.error("Error fetching activity:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Create a new activity
     */
    async createActivity(data: FieldActivityCreate): Promise<FieldActivity> {
      this.loading = true;
      this.error = null;

      try {
        const newActivity = await fieldActivityService.createActivity(data);
        this.activities.unshift(newActivity); // Add to beginning
        return newActivity;
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to create activity";
        console.error("Error creating activity:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update an existing activity
     */
    async updateActivity(
      activityId: number,
      workspaceId: number,
      data: FieldActivityUpdate,
    ): Promise<FieldActivity> {
      this.loading = true;
      this.error = null;

      try {
        const updatedActivity = await fieldActivityService.updateActivity(
          activityId,
          workspaceId,
          data,
        );

        // Update in list
        const index = this.activities.findIndex((act) => act.id === activityId);
        if (index !== -1) {
          this.activities[index] = updatedActivity;
        }

        // Update current activity if it's the same one
        if (this.currentActivity && this.currentActivity.id === activityId) {
          this.currentActivity = {
            ...this.currentActivity,
            ...updatedActivity,
          };
        }

        return updatedActivity;
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to update activity";
        console.error("Error updating activity:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete an activity
     */
    async deleteActivity(activityId: number, workspaceId: number) {
      this.loading = true;
      this.error = null;

      try {
        await fieldActivityService.deleteActivity(activityId, workspaceId);
        this.activities = this.activities.filter(
          (act) => act.id !== activityId,
        );
        if (this.currentActivity?.id === activityId) {
          this.currentActivity = null;
        }
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to delete activity";
        console.error("Error deleting activity:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch analytics data (manager/executive only)
     */
    async fetchAnalytics(
      workspaceId: number,
      dateFrom?: string,
      dateTo?: string,
    ) {
      this.loading = true;
      this.error = null;

      try {
        this.analytics = await fieldActivityService.getAnalytics(
          workspaceId,
          dateFrom,
          dateTo,
        );
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to fetch analytics";
        console.error("Error fetching analytics:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Upload a photo to an activity
     */
    async uploadPhoto(
      activityId: number,
      workspaceId: number,
      file: File,
    ): Promise<number> {
      this.loading = true;
      this.error = null;

      try {
        const result = await fieldActivityService.uploadPhoto(
          activityId,
          workspaceId,
          file,
        );

        // Refresh current activity if it's loaded
        if (this.currentActivity && this.currentActivity.id === activityId) {
          await this.fetchActivity(activityId, workspaceId);
        }

        return result.photo_id;
      } catch (error: any) {
        this.error = error.response?.data?.detail || "Failed to upload photo";
        console.error("Error uploading photo:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete a photo from an activity
     */
    async deletePhoto(
      activityId: number,
      photoId: number,
      workspaceId: number,
    ) {
      this.loading = true;
      this.error = null;

      try {
        await fieldActivityService.deletePhoto(
          activityId,
          photoId,
          workspaceId,
        );

        // Remove photo from current activity if loaded
        if (this.currentActivity && this.currentActivity.id === activityId) {
          this.currentActivity.photos = this.currentActivity.photos.filter(
            (photo) => photo.id !== photoId,
          );
        }
      } catch (error: any) {
        this.error = error.response?.data?.detail || "Failed to delete photo";
        console.error("Error deleting photo:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update filters and refetch
     */
    async setFilters(workspaceId: number, filters: FieldActivityFilters) {
      this.filters = filters;
      await this.fetchActivities(workspaceId, filters);
    },

    /**
     * Clear filters
     */
    async clearFilters(workspaceId: number) {
      this.filters = {};
      await this.fetchActivities(workspaceId);
    },

    /**
     * Clear all data (on logout or workspace switch)
     */
    clearAll() {
      this.activities = [];
      this.currentActivity = null;
      this.analytics = null;
      this.filters = {};
      this.currentWorkspaceId = null;
      this.error = null;
    },
  },
});
