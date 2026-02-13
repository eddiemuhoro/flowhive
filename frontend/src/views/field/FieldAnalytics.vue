<!-- Field Analytics View -->
<!-- Dashboard for viewing field activity statistics and insights -->

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Field Analytics</h1>
      <p class="mt-1 text-sm text-gray-500">
        Overview of field activities and team performance
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div
        class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
      ></div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="rounded-lg bg-red-50 border border-red-200 p-4"
    >
      <p class="text-sm text-red-800">
        Failed to load analytics. Please try again later.
      </p>
    </div>

    <!-- Analytics Content -->
    <div v-else-if="analytics" class="space-y-6">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Total Activities -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Total Activities
                  </dt>
                  <dd class="text-2xl font-bold text-gray-900">
                    {{ analytics.total_activities }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Hours -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Total Hours
                  </dt>
                  <dd class="text-2xl font-bold text-gray-900">
                    {{ analytics.total_hours.toFixed(1) }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- This Week -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    This Week
                  </dt>
                  <dd class="text-2xl font-bold text-gray-900">
                    {{ analytics.activities_this_week }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- This Month -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-orange-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    This Month
                  </dt>
                  <dd class="text-2xl font-bold text-gray-900">
                    {{ analytics.activities_this_month }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Top Staff -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            Top Performers
          </h3>
          <div v-if="analytics.top_staff.length > 0" class="space-y-4">
            <div
              v-for="(staff, index) in analytics.top_staff"
              :key="staff.user_id"
              class="flex items-center"
            >
              <!-- Rank Badge -->
              <div
                class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                :class="{
                  'bg-yellow-100 text-yellow-800': index === 0,
                  'bg-gray-100 text-gray-600': index === 1,
                  'bg-orange-100 text-orange-600': index === 2,
                  'bg-blue-50 text-blue-600': index > 2,
                }"
              >
                {{ index + 1 }}
              </div>

              <!-- Staff Info -->
              <div class="ml-3 flex-1">
                <p class="text-sm font-medium text-gray-900">
                  {{ staff.name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ staff.activity_count }} activities
                </p>
              </div>

              <!-- Progress Bar -->
              <div class="ml-4 flex-shrink-0 w-32">
                <div class="bg-gray-200 rounded-full h-2">
                  <div
                    class="rounded-full h-2 transition-all"
                    :class="{
                      'bg-yellow-500': index === 0,
                      'bg-gray-400': index === 1,
                      'bg-orange-400': index === 2,
                      'bg-blue-500': index > 2,
                    }"
                    :style="{
                      width: `${(staff.activity_count / analytics.top_staff[0].activity_count) * 100}%`,
                    }"
                  ></div>
                </div>
              </div>

              <!-- Count -->
              <div class="ml-3 text-sm font-semibold text-gray-700">
                {{ staff.activity_count }}
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-sm text-gray-500">
            No activity data available
          </div>
        </div>

        <!-- Category Distribution -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            Category Distribution
          </h3>
          <div v-if="categoryEntries.length > 0" class="space-y-3">
            <div
              v-for="[category, count] in categoryEntries"
              :key="category"
              class="flex items-center"
            >
              <!-- Category Name -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ category }}
                </p>
              </div>

              <!-- Bar Chart -->
              <div class="ml-4 flex-1 max-w-xs">
                <div class="flex items-center">
                  <div class="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      class="bg-blue-600 rounded-full h-2 transition-all"
                      :style="{
                        width: `${(count / maxCategoryCount) * 100}%`,
                      }"
                    ></div>
                  </div>
                  <span class="ml-3 text-sm font-semibold text-gray-700 w-8 text-right">
                    {{ count }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-sm text-gray-500">
            No category data available
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Average Hours per Activity -->
          <div>
            <p class="text-sm text-gray-500">Average Hours per Activity</p>
            <p class="mt-1 text-2xl font-bold text-gray-900">
              {{ averageHoursPerActivity }}
            </p>
          </div>

          <!-- Team Members Active -->
          <div>
            <p class="text-sm text-gray-500">Active Team Members</p>
            <p class="mt-1 text-2xl font-bold text-gray-900">
              {{ analytics.top_staff.length }}
            </p>
          </div>

          <!-- Categories Used -->
          <div>
            <p class="text-sm text-gray-500">Categories in Use</p>
            <p class="mt-1 text-2xl font-bold text-gray-900">
              {{ categoryEntries.length }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useWorkspaceStore } from "@/stores/workspace";
import { analyticsService } from "@/services/analytics.service";

const workspaceStore = useWorkspaceStore();

const currentWorkspaceId = computed(
  () => workspaceStore.currentWorkspace?.id || 0,
);

// Fetch analytics data with TanStack Query
const {
  data: analytics,
  isLoading,
  error,
} = useQuery({
  queryKey: ["field-analytics", currentWorkspaceId],
  queryFn: () => analyticsService.getFieldActivityAnalytics(currentWorkspaceId.value),
  enabled: computed(() => !!currentWorkspaceId.value),
  staleTime: 2 * 60 * 1000, // 2 minutes cache
});

// Computed properties for category distribution
const categoryEntries = computed(() => {
  if (!analytics.value?.category_distribution) return [];
  return Object.entries(analytics.value.category_distribution).sort(
    (a, b) => b[1] - a[1],
  );
});

const maxCategoryCount = computed(() => {
  if (categoryEntries.value.length === 0) return 1;
  return Math.max(...categoryEntries.value.map(([, count]) => count));
});

// Computed property for average hours
const averageHoursPerActivity = computed(() => {
  if (!analytics.value || analytics.value.total_activities === 0) {
    return "0.0";
  }
  return (analytics.value.total_hours / analytics.value.total_activities).toFixed(1);
});
</script>
