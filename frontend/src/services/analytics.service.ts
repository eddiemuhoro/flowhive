import { apiClient } from "./api";
import type {
  TaskAnalytics,
  ProjectAnalytics,
  UserProductivity,
  ExecutiveDashboard,
  FieldActivityAnalytics,
} from "@/types/analytics";

class AnalyticsService {
  /**
   * Get task analytics overview
   */
  async getTaskAnalytics(workspaceId?: number): Promise<TaskAnalytics> {
    const params = workspaceId ? { workspace_id: workspaceId } : {};
    const response = await apiClient.get<TaskAnalytics>("/analytics/overview", {
      params,
    });
    return response.data;
  }

  /**
   * Get field activity analytics for a workspace
   */
  async getFieldActivityAnalytics(
    workspaceId: number,
  ): Promise<FieldActivityAnalytics> {
    const response = await apiClient.get<FieldActivityAnalytics>(
      `/analytics/field-activities/overview`,
      {
        params: { workspace_id: workspaceId },
      },
    );
    return response.data;
  }

  /**
   * Get analytics for a specific project
   */
  async getProjectAnalytics(projectId: number): Promise<ProjectAnalytics> {
    const response = await apiClient.get<ProjectAnalytics>(
      `/analytics/projects/${projectId}`,
    );
    return response.data;
  }

  /**
   * Get user productivity metrics
   */
  async getUserProductivity(
    workspaceId?: number,
    limit: number = 10,
  ): Promise<UserProductivity[]> {
    const params: { workspace_id?: number; limit: number } = { limit };
    if (workspaceId) {
      params.workspace_id = workspaceId;
    }
    const response = await apiClient.get<UserProductivity[]>(
      "/analytics/user-productivity",
      { params },
    );
    return response.data;
  }

  /**
   * Get executive dashboard (Executive role only)
   */
  async getExecutiveDashboard(): Promise<ExecutiveDashboard> {
    const response =
      await apiClient.get<ExecutiveDashboard>("/analytics/executive-dashboard");
    return response.data;
  }
}

export const analyticsService = new AnalyticsService();
