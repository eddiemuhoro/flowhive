// Task Category Service
// Handles CRUD operations for field operations task categories

import { apiClient } from "./api";
import type {
  TaskCategory,
  TaskCategoryCreate,
  TaskCategoryUpdate,
} from "@/types/field";

export const taskCategoryService = {
  /**
   * Get all task categories for a workspace
   * @param workspaceId - The workspace ID
   * @param includeInactive - Whether to include inactive categories
   */
  async getCategories(
    workspaceId: number,
    includeInactive: boolean = false,
  ): Promise<TaskCategory[]> {
    const response = await apiClient.get<TaskCategory[]>(
      "/api/task-categories",
      {
        params: {
          workspace_id: workspaceId,
          include_inactive: includeInactive,
        },
      },
    );
    return response.data;
  },

  /**
   * Get a single task category by ID
   * @param categoryId - The category ID
   * @param workspaceId - The workspace ID for validation
   */
  async getCategory(
    categoryId: number,
    workspaceId: number,
  ): Promise<TaskCategory> {
    const response = await apiClient.get<TaskCategory>(
      `/api/task-categories/${categoryId}`,
      {
        params: { workspace_id: workspaceId },
      },
    );
    return response.data;
  },

  /**
   * Create a new task category
   * @param data - Category creation data
   */
  async createCategory(data: TaskCategoryCreate): Promise<TaskCategory> {
    const response = await apiClient.post<TaskCategory>(
      "/api/task-categories",
      data,
    );
    return response.data;
  },

  /**
   * Update an existing task category
   * @param categoryId - The category ID
   * @param workspaceId - The workspace ID for validation
   * @param data - Category update data
   */
  async updateCategory(
    categoryId: number,
    workspaceId: number,
    data: TaskCategoryUpdate,
  ): Promise<TaskCategory> {
    const response = await apiClient.put<TaskCategory>(
      `/api/task-categories/${categoryId}`,
      data,
      {
        params: { workspace_id: workspaceId },
      },
    );
    return response.data;
  },

  /**
   * Soft delete a task category (sets is_active to false)
   * @param categoryId - The category ID
   * @param workspaceId - The workspace ID for validation
   */
  async deleteCategory(categoryId: number, workspaceId: number): Promise<void> {
    await apiClient.delete(`/api/task-categories/${categoryId}`, {
      params: { workspace_id: workspaceId },
    });
  },
};
