<!-- Activity List Component -->
<!-- Displays a list of field activities grouped by date -->

<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="rounded-lg bg-white p-4 shadow-sm">
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <!-- Date From -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >From Date</label
          >
          <input
            v-model="filters.date_from"
            type="date"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </div>

        <!-- Date To -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >To Date</label
          >
          <input
            v-model="filters.date_to"
            type="date"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </div>

        <!-- Category Filter -->
        <div>
          <CategorySelector
            v-model="filters.task_category_id"
            :workspace-id="workspaceId"
            label="Category"
            placeholder="All categories"
            :allow-null="true"
          />
        </div>

        <!-- Customer Search -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Customer</label
          >
          <input
            v-model="filters.customer_name"
            type="text"
            placeholder="Search customer..."
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          />
        </div>
      </div>

      <!-- Filter Actions -->
      <div class="mt-4 flex items-center justify-between">
        <button
          @click="clearFilters"
          class="text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          Clear Filters
        </button>
        <button
          @click="applyFilters"
          :disabled="loading"
          class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Apply Filters
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div
          class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
        ></div>
        <p class="mt-2 text-sm text-gray-600">Loading activities...</p>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="activities.length === 0"
      class="rounded-lg bg-white p-12 text-center shadow-sm"
    >
      <svg
        class="mx-auto h-12 w-12 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">
        No activities found
      </h3>
      <p class="mt-1 text-sm text-gray-500">
        {{
          hasActiveFilters
            ? "Try adjusting your filters"
            : "Get started by creating your first activity"
        }}
      </p>
    </div>

    <!-- Activity Groups by Date -->
    <div v-else class="space-y-6">
      <div v-for="(group, date) in groupedActivities" :key="date">
        <!-- Date Header -->
        <div
          class="sticky top-0 z-10 flex items-center justify-between bg-gray-50 px-4 py-2 rounded-lg"
        >
          <h3 class="text-sm font-semibold text-gray-900">
            {{ formatDate(date) }}
          </h3>
          <span class="text-xs text-gray-500">
            {{ group.length }}
            {{ group.length === 1 ? "activity" : "activities" }}
          </span>
        </div>

        <!-- Activity Cards -->
        <div class="space-y-3">
          <ActivityCard
            v-for="activity in group"
            :key="activity.id"
            :activity="activity"
            :show-description="true"
            :show-actions="true"
            @view="handleView"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>
    </div>

    <!-- Load More (if implementing pagination) -->
    <div v-if="hasMore" class="text-center">
      <button
        @click="loadMore"
        :disabled="loading"
        class="rounded-lg border border-gray-300 px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
      >
        Load More
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ActivityCard from "./ActivityCard.vue";
import CategorySelector from "@/components/field/category/CategorySelector.vue";
import type { FieldActivity, FieldActivityFilters } from "@/types/field";

interface Props {
  activities: FieldActivity[];
  workspaceId: number;
  loading?: boolean;
  hasMore?: boolean;
}

interface Emits {
  (e: "view", activityId: number): void;
  (e: "edit", activityId: number): void;
  (e: "delete", activityId: number): void;
  (e: "filter", filters: FieldActivityFilters): void;
  (e: "loadMore"): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  hasMore: false,
});

const emit = defineEmits<Emits>();

const filters = ref<FieldActivityFilters>({
  date_from: undefined,
  date_to: undefined,
  task_category_id: undefined,
  customer_name: undefined,
});

const hasActiveFilters = computed(() => {
  return !!(
    filters.value.date_from ||
    filters.value.date_to ||
    filters.value.task_category_id ||
    filters.value.customer_name
  );
});

const groupedActivities = computed(() => {
  const groups: Record<string, FieldActivity[]> = {};

  props.activities.forEach((activity) => {
    if (!groups[activity.activity_date]) {
      groups[activity.activity_date] = [];
    }
    groups[activity.activity_date].push(activity);
  });

  // Sort activities within each group by start time
  Object.keys(groups).forEach((date) => {
    groups[date].sort((a, b) => {
      return a.start_time.localeCompare(b.start_time);
    });
  });

  return groups;
});

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const dateOnly = date.toDateString();
  const todayOnly = today.toDateString();
  const yesterdayOnly = yesterday.toDateString();

  if (dateOnly === todayOnly) {
    return "Today";
  } else if (dateOnly === yesterdayOnly) {
    return "Yesterday";
  }

  return date.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const applyFilters = () => {
  const cleanFilters: FieldActivityFilters = {};

  if (filters.value.date_from) cleanFilters.date_from = filters.value.date_from;
  if (filters.value.date_to) cleanFilters.date_to = filters.value.date_to;
  if (filters.value.task_category_id)
    cleanFilters.task_category_id = filters.value.task_category_id;
  if (filters.value.customer_name?.trim())
    cleanFilters.customer_name = filters.value.customer_name.trim();

  emit("filter", cleanFilters);
};

const clearFilters = () => {
  filters.value = {
    date_from: undefined,
    date_to: undefined,
    task_category_id: undefined,
    customer_name: undefined,
  };
  emit("filter", {});
};

const handleView = (activityId: number) => {
  emit("view", activityId);
};

const handleEdit = (activityId: number) => {
  emit("edit", activityId);
};

const handleDelete = (activityId: number) => {
  emit("delete", activityId);
};

const loadMore = () => {
  emit("loadMore");
};
</script>
