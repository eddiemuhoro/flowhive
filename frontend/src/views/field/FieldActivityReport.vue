<!-- Field Activity Report View -->
<!-- Dedicated page for viewing detailed activity reports, ideal for Monday meetings -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header with Print Controls -->
      <div class="flex items-start justify-between print:hidden">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Activity Report</h1>
          <p class="mt-1 text-sm text-gray-600">
            Detailed view for meeting reviews
          </p>
        </div>
        <div class="flex items-center space-x-3">
          <button
            @click="router.push('/field/activities')"
            class="flex items-center space-x-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
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
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            <span>Back to List</span>
          </button>
          <button
            @click="handlePrint"
            class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
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
                d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
              />
            </svg>
            <span>Print / Save PDF</span>
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="rounded-lg bg-white p-4 shadow-sm print:hidden">
        <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
          <!-- Staff Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Staff Member</label
            >
            <select
              v-model="selectedStaffId"
              @change="updateUrlParams"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            >
              <option :value="undefined">All staff members</option>
              <option
                v-for="member in currentWorkspace?.members || []"
                :key="member.user_id"
                :value="member.user_id"
              >
                {{ member.full_name || member.username }}
              </option>
            </select>
          </div>

          <!-- Date From -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >From Date</label
            >
            <input
              v-model="dateFrom"
              @change="updateUrlParams"
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
              v-model="dateTo"
              @change="updateUrlParams"
              type="date"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
        </div>

        <!-- Quick Filters -->
        <div class="mt-3 flex items-center space-x-2">
          <span class="text-xs font-medium text-gray-700">Quick:</span>
          <button
            @click="setLastWeekComplete"
            class="rounded px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
          >
            Last Week
          </button>
          <button
            @click="setLast7Days"
            class="rounded px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
          >
            Last 7 Days
          </button>
          <button
            @click="setThisWeek"
            class="rounded px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
          >
            This Week
          </button>
          <button
            @click="setLastMonth"
            class="rounded px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
          >
            Last 30 Days
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div
            class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
          <p class="mt-2 text-sm text-gray-600">Loading report...</p>
        </div>
      </div>

      <!-- Report Content -->
      <div v-else-if="filteredActivities.length > 0">
        <!-- Summary Section -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Report Summary
          </h2>
          <div class="grid grid-cols-2 gap-6 md:grid-cols-4">
            <div>
              <p class="text-sm text-gray-600">Total Activities</p>
              <p class="mt-1 text-2xl font-bold text-gray-900">
                {{ reportSummary.totalActivities }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Total Hours</p>
              <p class="mt-1 text-2xl font-bold text-gray-900">
                {{ reportSummary.totalHours.toFixed(1) }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Customers Served</p>
              <p class="mt-1 text-2xl font-bold text-gray-900">
                {{ reportSummary.uniqueCustomers }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Staff Members</p>
              <p class="mt-1 text-2xl font-bold text-gray-900">
                {{ reportSummary.uniqueStaff }}
              </p>
            </div>
          </div>

          <!-- Category Breakdown -->
          <div v-if="reportSummary.categoryBreakdown.length > 0" class="mt-6">
            <h3 class="text-sm font-semibold text-gray-900 mb-3">
              By Category
            </h3>
            <div class="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
              <div
                v-for="cat in reportSummary.categoryBreakdown"
                :key="cat.name"
                class="flex items-center justify-between rounded-lg border border-gray-200 p-3"
              >
                <div class="flex items-center space-x-2">
                  <div
                    class="h-3 w-3 rounded-full"
                    :style="{ backgroundColor: cat.color }"
                  ></div>
                  <span class="text-sm font-medium text-gray-900">{{
                    cat.title
                  }}</span>
                </div>
                <span class="text-sm text-gray-600"
                  >{{ cat.count }} ({{ cat.hours.toFixed(1) }}h)</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Activities -->
        <div class="space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">
            Detailed Activities
          </h2>

          <!-- Group by Staff if not filtered -->
          <div v-if="!selectedStaffId" class="space-y-6">
            <div
              v-for="(staffGroup, staffId) in groupedByStaff"
              :key="staffId"
              class="space-y-3"
            >
              <!-- Staff Header -->
              <div
                class="sticky top-0 z-10 rounded-lg bg-blue-50 p-3 print:relative"
              >
                <h3 class="font-semibold text-gray-900">
                  {{ staffGroup.name }}
                </h3>
                <p class="text-sm text-gray-600">
                  {{ staffGroup.activities.length }} activities ·
                  {{ staffGroup.totalHours.toFixed(1) }} hours
                </p>
              </div>

              <!-- Staff Activities -->
              <div class="space-y-3">
                <ActivityDetailCard
                  v-for="(activity, index) in staffGroup.activities"
                  :key="activity.id"
                  :activity="activity"
                  :index="index + 1"
                />
              </div>
            </div>
          </div>

          <!-- Ungrouped if filtered by staff -->
          <div v-else class="space-y-3">
            <ActivityDetailCard
              v-for="(activity, index) in sortedActivities"
              :key="activity.id"
              :activity="activity"
              :index="index + 1"
            />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else
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
          Try adjusting your date range or staff filters
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useWorkspaceStore } from "@/stores/workspace";
import { useFieldActivities } from "@/composables/useFieldActivities";
import ActivityDetailCard from "@/components/field/activity/ActivityDetailCard.vue";
import type { FieldActivityFilters } from "@/types/field";

const router = useRouter();
const route = useRoute();
const workspaceStore = useWorkspaceStore();

const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);

// Filter state
const selectedStaffId = ref<number | undefined>(undefined);
const dateFrom = ref<string | undefined>(undefined);
const dateTo = ref<string | undefined>(undefined);

// Computed filters
const filters = computed<FieldActivityFilters>(() => ({
  support_staff_id: selectedStaffId.value,
  date_from: dateFrom.value,
  date_to: dateTo.value,
}));

// Fetch activities
const { data: activitiesData, isLoading } = useFieldActivities(
  currentWorkspaceId,
  filters
);

const filteredActivities = computed(() => activitiesData.value || []);

// Sort activities by date and time
const sortedActivities = computed(() => {
  return [...filteredActivities.value].sort((a, b) => {
    const dateCompare = a.activity_date.localeCompare(b.activity_date);
    if (dateCompare !== 0) return dateCompare;
    return (a.start_time || '').localeCompare(b.start_time || '');
  });
});

// Report summary calculations
const reportSummary = computed(() => {
  const activities = filteredActivities.value;
  const totalHours = activities.reduce(
    (sum, a) => sum + (a.duration_hours || 0),
    0
  );
  const uniqueCustomers = new Set(activities.map((a) => a.customer_name))
    .size;
  const uniqueStaff = new Set(activities.map((a) => a.support_staff_id)).size;

  // Category breakdown
  const categoryMap = new Map<
    string,
    { name: string; title: string; color: string; count: number; hours: number }
  >();

  activities.forEach((activity) => {
    if (activity.task_category) {
      const key = activity.task_category.name;
      const existing = categoryMap.get(key) || {
        name: activity.task_category.name,
        title: activity.task_category.title,
        color: activity.task_category.color,
        count: 0,
        hours: 0,
      };
      existing.count++;
      existing.hours += activity.duration_hours || 0;
      categoryMap.set(key, existing);
    }
  });

  return {
    totalActivities: activities.length,
    totalHours,
    uniqueCustomers,
    uniqueStaff,
    categoryBreakdown: Array.from(categoryMap.values()).sort(
      (a, b) => b.count - a.count
    ),
  };
});

// Group activities by staff
const groupedByStaff = computed(() => {
  const groups: Record<
    number,
    { name: string; activities: any[]; totalHours: number }
  > = {};

  sortedActivities.value.forEach((activity) => {
    if (!groups[activity.support_staff_id]) {
      groups[activity.support_staff_id] = {
        name: activity.support_staff_name,
        activities: [],
        totalHours: 0,
      };
    }
    groups[activity.support_staff_id].activities.push(activity);
    groups[activity.support_staff_id].totalHours +=
      activity.duration_hours || 0;
  });

  return groups;
});

// Quick date filters
const setLastWeekComplete = () => {
  const today = new Date();
  const currentDayOfWeek = today.getDay();

  // Calculate last week's Monday
  const lastMonday = new Date(today);
  const daysToLastMonday = currentDayOfWeek === 0 ? 13 : currentDayOfWeek + 6;
  lastMonday.setDate(lastMonday.getDate() - daysToLastMonday);

  // Calculate last week's Sunday
  const lastSunday = new Date(lastMonday);
  lastSunday.setDate(lastSunday.getDate() + 6);

  dateFrom.value = lastMonday.toISOString().split("T")[0];
  dateTo.value = lastSunday.toISOString().split("T")[0];
  updateUrlParams();
};

const setLast7Days = () => {
  const today = new Date();
  const lastWeek = new Date(today);
  lastWeek.setDate(lastWeek.getDate() - 7);

  dateFrom.value = lastWeek.toISOString().split("T")[0];
  dateTo.value = today.toISOString().split("T")[0];
  updateUrlParams();
};

const setThisWeek = () => {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const monday = new Date(today);
  monday.setDate(monday.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1));

  dateFrom.value = monday.toISOString().split("T")[0];
  dateTo.value = today.toISOString().split("T")[0];
  updateUrlParams();
};

const setLastMonth = () => {
  const today = new Date();
  const lastMonth = new Date(today);
  lastMonth.setDate(lastMonth.getDate() - 30);

  dateFrom.value = lastMonth.toISOString().split("T")[0];
  dateTo.value = today.toISOString().split("T")[0];
  updateUrlParams();
};

// Update URL with filter params (for sharing)
const updateUrlParams = () => {
  const params: Record<string, string> = {};

  if (selectedStaffId.value) {
    params.staff = String(selectedStaffId.value);
  }
  if (dateFrom.value) {
    params.from = dateFrom.value;
  }
  if (dateTo.value) {
    params.to = dateTo.value;
  }

  router.replace({
    query: Object.keys(params).length > 0 ? params : undefined,
  });
};

// Load filters from URL on mount
const loadFiltersFromUrl = () => {
  if (route.query.staff) {
    selectedStaffId.value = Number(route.query.staff);
  }
  if (route.query.from) {
    dateFrom.value = String(route.query.from);
  }
  if (route.query.to) {
    dateTo.value = String(route.query.to);
  }
};

// Print handler
const handlePrint = () => {
  window.print();
};

onMounted(() => {
  loadFiltersFromUrl();
});
</script>

<style scoped>
/* Print styles */
@media print {
  @page {
    margin: 1cm;
    size: A4;
  }

  body {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .print\:hidden {
    display: none !important;
  }

  .print\:relative {
    position: relative !important;
  }

  /* Ensure cards don't break across pages */
  .space-y-3 > * {
    page-break-inside: avoid;
    break-inside: avoid;
  }
}
</style>
