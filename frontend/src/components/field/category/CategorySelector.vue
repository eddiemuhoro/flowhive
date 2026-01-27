<!-- Category Selector Component -->
<!-- Dropdown for selecting task categories in forms -->

<template>
  <div class="relative">
    <label v-if="label" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <button
      type="button"
      @click="toggleDropdown"
      :disabled="disabled || loading"
      class="relative w-full cursor-pointer rounded-lg border bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100"
      :class="[
        error ? 'border-red-300' : 'border-gray-300',
        disabled ? 'opacity-60' : '',
      ]"
    >
      <span v-if="selectedCategory" class="flex items-center">
        <CategoryBadge
          :category="selectedCategory"
          :show-title="true"
          variant="light"
        />
      </span>
      <span v-else class="block truncate text-gray-400">
        {{ placeholder }}
      </span>

      <span
        class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
      >
        <svg
          class="h-5 w-5 text-gray-400"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </span>
    </button>

    <!-- Dropdown Menu -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      >
        <!-- Allow No Category Option -->
        <div
          v-if="allowNull"
          @click="selectCategory(null)"
          class="relative cursor-pointer select-none px-3 py-2 hover:bg-gray-100"
          :class="{ 'bg-blue-50': modelValue === null }"
        >
          <span class="block truncate text-gray-500 text-sm">No Category</span>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="px-3 py-2 text-center text-sm text-gray-500">
          Loading categories...
        </div>

        <!-- Empty State -->
        <div
          v-else-if="categories.length === 0"
          class="px-3 py-2 text-center text-sm text-gray-500"
        >
          No categories available
        </div>

        <!-- Category Options -->
        <div
          v-for="category in categories"
          :key="category.id"
          @click="selectCategory(category.id)"
          class="relative cursor-pointer select-none px-3 py-2 hover:bg-gray-100"
          :class="{ 'bg-blue-50': modelValue === category.id }"
        >
          <CategoryBadge
            :category="category"
            :show-title="true"
            variant="light"
          />
          <p
            v-if="category.description"
            class="mt-1 text-xs text-gray-500 truncate"
          >
            {{ category.description }}
          </p>
        </div>
      </div>
    </transition>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useTaskCategoryStore } from "@/stores/taskCategory";
import CategoryBadge from "./CategoryBadge.vue";

interface Props {
  modelValue: number | null | undefined;
  workspaceId: number;
  label?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  allowNull?: boolean;
  error?: string;
}

interface Emits {
  (e: "update:modelValue", value: number | null): void;
}

const props = withDefaults(defineProps<Props>(), {
  label: "",
  placeholder: "Select a category",
  required: false,
  disabled: false,
  allowNull: true,
  error: "",
});

const emit = defineEmits<Emits>();

const categoryStore = useTaskCategoryStore();
const isOpen = ref(false);

const categories = computed(() => categoryStore.activeCategories);
const loading = computed(() => categoryStore.loading);

const selectedCategory = computed(() => {
  if (!props.modelValue) return null;
  return categoryStore.getCategoryById(props.modelValue);
});

const toggleDropdown = () => {
  if (!props.disabled && !loading.value) {
    isOpen.value = !isOpen.value;
  }
};

const selectCategory = (categoryId: number | null) => {
  emit("update:modelValue", categoryId);
  isOpen.value = false;
};

const closeDropdown = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest(".relative")) {
    isOpen.value = false;
  }
};

onMounted(async () => {
  // Load categories if not already loaded
  if (categories.value.length === 0) {
    try {
      await categoryStore.fetchCategories(props.workspaceId);
    } catch (error) {
      console.error("Failed to load categories:", error);
    }
  }

  // Close dropdown when clicking outside
  document.addEventListener("click", closeDropdown);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", closeDropdown);
});
</script>
