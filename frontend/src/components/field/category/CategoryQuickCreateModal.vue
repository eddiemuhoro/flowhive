<!-- Category Quick Create Modal -->
<!-- Modal for quickly creating a new task category while filling out an activity form -->

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between border-b px-6 py-4">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Create Task Category</h2>
          <p class="text-sm text-gray-500 mt-1">Add a new category to organize field activities</p>
        </div>
        <button
          type="button"
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-500"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <!-- Helper Text -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <p class="text-xs text-blue-800">
            <strong>💡 Tip:</strong> Categories help organize different types of field work
            (e.g., Installation, Maintenance, Troubleshooting, Training).
            Check if a similar category exists before creating a new one.
          </p>
        </div>

        <!-- Category Title -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Category Name <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formData.title"
            type="text"
            required
            placeholder="e.g., Generator Repair, Network Setup"
            class="w-full rounded-lg border px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            :class="{ 'border-red-300': errors.title }"
          />
          <p v-if="errors.title" class="mt-1 text-xs text-red-600">{{ errors.title }}</p>
          <p class="mt-1 text-xs text-gray-500">Choose a clear, descriptive name that others will recognize</p>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Description (Optional)
          </label>
          <textarea
            v-model="formData.description"
            rows="2"
            placeholder="Help others understand when to use this category"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          ></textarea>
        </div>

        <!-- Color Picker -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Color <span class="text-red-500">*</span>
          </label>
          <div class="grid grid-cols-8 gap-2">
            <button
              v-for="color in colorOptions"
              :key="color"
              type="button"
              @click="formData.color = color"
              class="w-8 h-8 rounded-full border-2 transition-all"
              :style="{ backgroundColor: color }"
              :class="formData.color === color ? 'border-gray-800 scale-110' : 'border-gray-300 hover:scale-105'"
            >
              <span v-if="formData.color === color" class="text-white text-xs">✓</span>
            </button>
          </div>
          <p class="mt-1 text-xs text-gray-500">Pick a color for visual organization</p>
        </div>

        <!-- Visibility Info -->
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
          <p class="text-xs text-gray-600">
            <strong>📢 Visibility:</strong> This category will be visible to all team members in your workspace.
          </p>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-3 pt-4 border-t">
          <button
            type="button"
            @click="$emit('close')"
            :disabled="isCreating"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isCreating"
            class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <svg v-if="isCreating" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ isCreating ? 'Creating...' : 'Create Category' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useCreateTaskCategory } from '@/composables/useTaskCategories';
import { useTaskCategoryStore } from '@/stores/taskCategory';
import type { TaskCategoryCreate } from '@/types/field';

interface Props {
  workspaceId: number;
}

interface Emits {
  (e: 'close'): void;
  (e: 'created', categoryId: number): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const categoryStore = useTaskCategoryStore();

// Preset color options
const colorOptions = [
  '#3B82F6', // blue
  '#10B981', // green
  '#F59E0B', // amber
  '#EF4444', // red
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#14B8A6', // teal
  '#F97316', // orange
  '#6366F1', // indigo
  '#84CC16', // lime
  '#06B6D4', // cyan
  '#F43F5E', // rose
  '#A855F7', // violet
  '#22D3EE', // sky
  '#FB923C', // orange-400
  '#4ADE80', // green-400
];

const formData = ref<Omit<TaskCategoryCreate, 'name' | 'workspace_id'> & { title: string; description?: string; color: string }>({
  title: '',
  description: '',
  color: colorOptions[0],
  required_role: 'team_member', // Default to visible to everyone
});

const errors = ref<Record<string, string>>({});

const { mutate: createCategory, isPending: isCreating } = useCreateTaskCategory();

// Generate slug from title
const generateSlug = (title: string): string => {
  return title
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/\s+/g, '_') // Replace spaces with underscores
    .replace(/-+/g, '_'); // Replace multiple dashes with single underscore
};

const validateForm = (): boolean => {
  errors.value = {};

  if (!formData.value.title.trim()) {
    errors.value.title = 'Category name is required';
    return false;
  }

  if (formData.value.title.trim().length < 3) {
    errors.value.title = 'Category name must be at least 3 characters';
    return false;
  }

  return true;
};

const handleSubmit = () => {
  if (!validateForm()) {
    return;
  }

  const categoryData: TaskCategoryCreate = {
    name: generateSlug(formData.value.title),
    title: formData.value.title.trim(),
    description: formData.value.description?.trim() || '',
    color: formData.value.color,
    workspace_id: props.workspaceId,
    required_role: 'team_member', // Always team_member for staff-created categories
  };

  createCategory(categoryData, {
    onSuccess: (data) => {
      // Refresh Pinia store to update CategorySelector immediately
      categoryStore.fetchCategories(props.workspaceId);
      // TanStack Query cache is automatically invalidated by useCreateTaskCategory
      emit('created', data.id);
    },
    onError: (error: any) => {
      console.error('Failed to create category:', error);
      errors.value.title = error.response?.data?.detail || 'Failed to create category';
    },
  });
};
</script>
