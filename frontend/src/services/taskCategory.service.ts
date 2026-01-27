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
      `/task-categories/workspace/${workspaceId}`,
      {
        params: {
          include_inactive: includeInactive,
        },
      },
    );
    return response.data;
  },

  /**
   * Get a single task category by ID
   * @param categoryId - The category ID
   */
  async getCategory(
    categoryId: number,
  ): Promise<TaskCategory> {
    const response = await apiClient.get<TaskCategory>(
      `/task-categories/${categoryId}`,
    );
    return response.data;
  },

  /**
   * Create a new task category
   * @param data - Category creation data
   */
  async createCategory(data: TaskCategoryCreate): Promise<TaskCategory> {
    const response = await apiClient.post<TaskCategory>(
      "/task-categories",
      data,
    );
    return response.data;
  },

  /**
   * Update an existing task category
   * @param categoryId - The category ID
   * @param data - Category update data
   */
  async updateCategory(
    categoryId: number,
    data: TaskCategoryUpdate,
  ): Promise<TaskCategory> {
    const response = await apiClient.put<TaskCategory>(
      `/task-categories/${categoryId}`,
      data,
    );
    return response.data;
  },

  /**
   * Soft delete a task category (sets is_active to false)
   * @param categoryId - The category ID
   */
  async deleteCategory(categoryId: number): Promise<void> {
    await apiClient.delete(`/task-categories/${categoryId}`);
  },
};
