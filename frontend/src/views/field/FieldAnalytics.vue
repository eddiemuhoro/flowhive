<!-- Field Analytics View -->
<!-- Manager and Executive analytics dashboard for field operations -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header -->
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Field Analytics</h1>
        <p class="mt-1 text-sm text-gray-600">
          Team performance and activity insights
        </p>
      </div>

      <!-- Date Range Filter -->
      <div class="rounded-lg bg-white p-4 shadow-sm">
        <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >From Date</label
            >
            <input
              v-model="dateFrom"
              type="date"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >To Date</label
            >
            <input
              v-model="dateTo"
              type="date"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div class="flex items-end">
            <button
              @click="loadAnalytics"
              :disabled="loading"
              class="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {{ loading ? "Loading..." : "Update Analytics" }}
            </button>
          </div>
        </div>

        <!-- Quick Date Filters -->
        <div class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="preset in datePresets"
            :key="preset.label"
            @click="applyDatePreset(preset)"
            class="rounded-lg border border-gray-300 px-3 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
          >
            {{ preset.label }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div
            class="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
          <p class="mt-2 text-sm text-gray-600">Loading analytics...</p>
        </div>
      </div>

      <!-- Analytics Content -->
      <template v-else-if="analytics">
        <!-- Summary Stats -->
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div class="rounded-lg bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">
                  Total Activities
                </p>
                <p class="mt-2 text-3xl font-bold text-gray-900">
                  {{ analytics.total_activities }}
                </p>
              </div>
              <div class="rounded-full bg-blue-100 p-3">
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
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div class="rounded-lg bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Total Hours</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">
                  {{ analytics.total_hours.toFixed(1) }}
                </p>
              </div>
              <div class="rounded-full bg-green-100 p-3">
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
            </div>
          </div>

          <div class="rounded-lg bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">
                  Avg Hours/Activity
                </p>
                <p class="mt-2 text-3xl font-bold text-gray-900">
                  {{
                    analytics.total_activities > 0
                      ? (
                          analytics.total_hours / analytics.total_activities
                        ).toFixed(1)
                      : "0.0"
                  }}
                </p>
              </div>
              <div class="rounded-full bg-purple-100 p-3">
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
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Hours by Staff -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Hours by Staff Member
          </h2>
          <div v-if="analytics.hours_by_staff.length > 0" class="space-y-3">
            <div
              v-for="staff in sortedStaffHours"
              :key="staff.staff_id"
              class="flex items-center justify-between rounded-lg border border-gray-200 p-4"
            >
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ staff.staff_name }}</p>
                <p class="text-sm text-gray-500">
                  {{ staff.activity_count }} activities
                </p>
              </div>
              <div class="text-right">
                <p class="text-xl font-bold text-gray-900">
                  {{ staff.total_hours.toFixed(1) }}h
                </p>
                <div
                  class="mt-1 h-2 w-32 overflow-hidden rounded-full bg-gray-200"
                >
                  <div
                    class="h-full bg-blue-600"
                    :style="{
                      width: `${(staff.total_hours / maxStaffHours) * 100}%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-sm text-gray-500">
            No staff data available for the selected period
          </div>
        </div>

        <!-- Activities by Category -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Activities by Category
          </h2>
          <div
            v-if="analytics.activities_by_category.length > 0"
            class="space-y-3"
          >
            <div
              v-for="category in sortedCategoryStats"
              :key="category.category_id ?? 'uncategorized'"
              class="flex items-center justify-between rounded-lg border border-gray-200 p-4"
            >
              <div class="flex-1">
                <p class="font-medium text-gray-900">
                  {{ category.category_title || "Uncategorized" }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ category.total_hours.toFixed(1) }} hours
                </p>
              </div>
              <div class="text-right">
                <p class="text-xl font-bold text-gray-900">
                  {{ category.activity_count }}
                </p>
                <div
                  class="mt-1 h-2 w-32 overflow-hidden rounded-full bg-gray-200"
                >
                  <div
                    class="h-full bg-green-600"
                    :style="{
                      width: `${(category.activity_count / maxCategoryCount) * 100}%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-sm text-gray-500">
            No category data available for the selected period
          </div>
        </div>

        <!-- Export Button -->
        <div class="flex justify-end">
          <button
            @click="exportToExcel"
            class="flex items-center space-x-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>Export to Excel</span>
          </button>
        </div>
      </template>

      <!-- Empty State -->
      <div v-else class="rounded-lg bg-white p-12 text-center shadow-sm">
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
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">
          No Analytics Data
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          Select a date range to view analytics
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import { useFieldActivityStore } from "@/stores/fieldActivity";

const workspaceStore = useWorkspaceStore();
const activityStore = useFieldActivityStore();

const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);
const analytics = computed(() => activityStore.analytics);

const loading = ref(false);
const dateFrom = ref("");
const dateTo = ref("");

interface DatePreset {
  label: string;
  getDates: () => { from: string; to: string };
}

const datePresets: DatePreset[] = [
  {
    label: "Today",
    getDates: () => {
      const today = new Date().toISOString().split("T")[0];
      return { from: today, to: today };
    },
  },
  {
    label: "Last 7 Days",
    getDates: () => {
      const to = new Date();
      const from = new Date(to.getTime() - 7 * 24 * 60 * 60 * 1000);
      return {
        from: from.toISOString().split("T")[0],
        to: to.toISOString().split("T")[0],
      };
    },
  },
  {
    label: "Last 30 Days",
    getDates: () => {
      const to = new Date();
      const from = new Date(to.getTime() - 30 * 24 * 60 * 60 * 1000);
      return {
        from: from.toISOString().split("T")[0],
        to: to.toISOString().split("T")[0],
      };
    },
  },
  {
    label: "This Month",
    getDates: () => {
      const now = new Date();
      const from = new Date(now.getFullYear(), now.getMonth(), 1);
      const to = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      return {
        from: from.toISOString().split("T")[0],
        to: to.toISOString().split("T")[0],
      };
    },
  },
  {
    label: "Last Month",
    getDates: () => {
      const now = new Date();
      const from = new Date(now.getFullYear(), now.getMonth() - 1, 1);
      const to = new Date(now.getFullYear(), now.getMonth(), 0);
      return {
        from: from.toISOString().split("T")[0],
        to: to.toISOString().split("T")[0],
      };
    },
  },
];

const sortedStaffHours = computed(() => {
  if (!analytics.value) return [];
  return [...analytics.value.hours_by_staff].sort(
    (a, b) => b.total_hours - a.total_hours,
  );
});

const sortedCategoryStats = computed(() => {
  if (!analytics.value) return [];
  return [...analytics.value.activities_by_category].sort(
    (a, b) => b.activity_count - a.activity_count,
  );
});

const maxStaffHours = computed(() => {
  if (!analytics.value || analytics.value.hours_by_staff.length === 0) return 0;
  return Math.max(...analytics.value.hours_by_staff.map((s) => s.total_hours));
});

const maxCategoryCount = computed(() => {
  if (!analytics.value || analytics.value.activities_by_category.length === 0)
    return 0;
  return Math.max(
    ...analytics.value.activities_by_category.map((c) => c.activity_count),
  );
});

const applyDatePreset = (preset: DatePreset) => {
  const dates = preset.getDates();
  dateFrom.value = dates.from;
  dateTo.value = dates.to;
  loadAnalytics();
};

const loadAnalytics = async () => {
  if (!currentWorkspaceId.value) return;

  loading.value = true;
  try {
    await activityStore.fetchAnalytics(
      currentWorkspaceId.value,
      dateFrom.value || undefined,
      dateTo.value || undefined,
    );
  } catch (error: any) {
    console.error("Failed to load analytics:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to load analytics. Please try again.",
    );
  } finally {
    loading.value = false;
  }
};

const exportToExcel = () => {
  // TODO: Implement Excel export functionality
  alert("Excel export feature coming soon!");
};

onMounted(() => {
  // Default to last 30 days
  const preset = datePresets[2]; // Last 30 Days
  const dates = preset.getDates();
  dateFrom.value = dates.from;
  dateTo.value = dates.to;
  loadAnalytics();
});
</script>
