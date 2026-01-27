// Task Category Store (Field Operations)
// Manages task categories for field operations workspaces

import { defineStore } from "pinia";
import { taskCategoryService } from "@/services/taskCategory.service";
import type {
  TaskCategory,
  TaskCategoryCreate,
  TaskCategoryUpdate,
} from "@/types/field";

interface TaskCategoryState {
  categories: TaskCategory[];
  loading: boolean;
  error: string | null;
  currentWorkspaceId: number | null;
}

export const useTaskCategoryStore = defineStore("taskCategory", {
  state: (): TaskCategoryState => ({
    categories: [],
    loading: false,
    error: null,
    currentWorkspaceId: null,
  }),

  getters: {
    /**
     * Get only active categories
     */
    activeCategories: (state): TaskCategory[] => {
      return state.categories.filter((cat) => cat.is_active);
    },

    /**
     * Get category by ID
     */
    getCategoryById:
      (state) =>
      (id: number): TaskCategory | undefined => {
        return state.categories.find((cat) => cat.id === id);
      },

    /**
     * Check if categories are loaded for current workspace
     */
    isLoaded: (state): boolean => {
      return state.categories.length > 0 && !state.loading;
    },
  },

  actions: {
    /**
     * Fetch all categories for a workspace
     */
    async fetchCategories(
      workspaceId: number,
      includeInactive: boolean = false,
    ) {
      this.loading = true;
      this.error = null;
      this.currentWorkspaceId = workspaceId;

      try {
        this.categories = await taskCategoryService.getCategories(
          workspaceId,
          includeInactive,
        );
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to fetch task categories";
        console.error("Error fetching categories:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Create a new category
     */
    async createCategory(data: TaskCategoryCreate): Promise<TaskCategory> {
      this.loading = true;
      this.error = null;

      try {
        const newCategory = await taskCategoryService.createCategory(data);
        this.categories.push(newCategory);
        return newCategory;
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to create task category";
        console.error("Error creating category:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update an existing category
     */
    async updateCategory(
      categoryId: number,
      workspaceId: number,
      data: TaskCategoryUpdate,
    ): Promise<TaskCategory> {
      this.loading = true;
      this.error = null;

      try {
        const updatedCategory = await taskCategoryService.updateCategory(
          categoryId,
          workspaceId,
          data,
        );
        const index = this.categories.findIndex((cat) => cat.id === categoryId);
        if (index !== -1) {
          this.categories[index] = updatedCategory;
        }
        return updatedCategory;
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to update task category";
        console.error("Error updating category:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Soft delete a category
     */
    async deleteCategory(categoryId: number, workspaceId: number) {
      this.loading = true;
      this.error = null;

      try {
        await taskCategoryService.deleteCategory(categoryId, workspaceId);
        // Update the local state to mark as inactive
        const category = this.categories.find((cat) => cat.id === categoryId);
        if (category) {
          category.is_active = false;
        }
      } catch (error: any) {
        this.error =
          error.response?.data?.detail || "Failed to delete task category";
        console.error("Error deleting category:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Clear all categories (on logout or workspace switch)
     */
    clearCategories() {
      this.categories = [];
      this.currentWorkspaceId = null;
      this.error = null;
    },
  },
});
