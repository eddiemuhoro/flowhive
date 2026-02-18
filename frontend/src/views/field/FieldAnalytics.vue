<!-- Field Analytics View -->
<!-- Dashboard for viewing field activity statistics and insights -->

<template>
  <div class="space-y-6 p-2 md:p-6">
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
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5">
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

        <!-- Customers Served -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Customers Served
                  </dt>
                  <dd class="text-2xl font-bold text-gray-900">
                    {{ analytics.unique_customers || 0 }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- Charts Row -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Top Staff -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            Top With Activities
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

        <!-- Top Customers -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            Top Customers
          </h3>
          <div v-if="topCustomers.length > 0" class="space-y-4">
            <div
              v-for="(customer, index) in topCustomers"
              :key="customer.customer_name"
              class="flex items-center"
            >
              <!-- Rank Badge -->
              <div
                class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                :class="{
                  'bg-yellow-100 text-yellow-800': index === 0,
                  'bg-gray-100 text-gray-600': index === 1,
                  'bg-orange-100 text-orange-600': index === 2,
                  'bg-indigo-50 text-indigo-600': index > 2,
                }"
              >
                {{ index + 1 }}
              </div>

              <!-- Customer Info -->
              <div class="ml-3 flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ customer.customer_name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ customer.visit_count }} activities
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
                      'bg-indigo-500': index > 2,
                    }"
                    :style="{
                      width: `${(customer.visit_count / topCustomers[0].visit_count) * 100}%`,
                    }"
                  ></div>
                </div>
              </div>

              <!-- Count -->
              <div class="ml-3 text-sm font-semibold text-gray-700">
                {{ customer.visit_count }}
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-sm text-gray-500">
            No customer data available
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
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

          <!-- Unique Customers -->
          <div>
            <p class="text-sm text-gray-500">Unique Customers</p>
            <p class="mt-1 text-2xl font-bold text-gray-900">
              {{ analytics.unique_customers || 0 }}
            </p>
          </div>
        </div>
      </div>
            <!-- Billing Metrics -->
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Billing Overview</h3>
          <div class="text-sm text-gray-500">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-2">
              On-Site = Billable
            </span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
              Office = Non-Billable
            </span>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
          <!-- Billable Hours -->
          <div>
            <p class="text-sm text-gray-600">Billable Hours</p>
            <p class="mt-1 text-2xl font-bold text-green-600">
              {{ analytics.billable_hours?.toFixed(1) || '0.0' }}h
            </p>
            <p class="text-xs text-gray-500">{{ analytics.billable_visits || 0 }} visits</p>
          </div>
          <!-- Non-Billable Hours -->
          <div>
            <p class="text-sm text-gray-600">Non-Billable Hours</p>
            <p class="mt-1 text-2xl font-bold text-gray-600">
              {{ analytics.non_billable_hours?.toFixed(1) || '0.0' }}h
            </p>
            <p class="text-xs text-gray-500">{{ analytics.office_activities || 0 }} tasks</p>
          </div>
          <!-- Billing Rate -->
          <div>
            <p class="text-sm text-gray-600">Billing Rate</p>
            <p class="mt-1 text-2xl font-bold text-blue-600">
              {{ analytics.billing_rate?.toFixed(1) || '0.0' }}%
            </p>
            <p class="text-xs text-gray-500">of total hours</p>
          </div>
          <!-- Visual Progress Bar -->
          <div class="col-span-2">
            <p class="text-sm text-gray-600 mb-2">Hours Breakdown</p>
            <div class="flex items-center space-x-2">
              <div class="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  class="bg-green-500 h-full transition-all duration-300"
                  :style="{ width: `${analytics.billing_rate || 0}%` }"
                ></div>
              </div>
              <div class="text-sm font-semibold text-gray-700 whitespace-nowrap">
                {{ analytics.billable_hours?.toFixed(1) || '0.0' }} / {{ analytics.total_hours?.toFixed(1) || '0.0' }}h
              </div>
            </div>
            <div class="mt-2 flex justify-between text-xs text-gray-500">
              <span>Billable: {{ analytics.billable_visits || 0 }} visits</span>
              <span>Office: {{ analytics.office_activities || 0 }} tasks</span>
            </div>
          </div>
        </div>
      </div>


      <!-- Recent On-Site Visits -->
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Recent On-Site Visits</h3>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Billable Activities
          </span>
        </div>

        <!-- Loading State -->
        <div v-if="activitiesLoading" class="flex items-center justify-center py-8">
          <div class="inline-block h-6 w-6 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
        </div>

        <!-- Activities List -->
        <div v-else-if="onSiteVisits.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Date</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Customer</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Location</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Staff</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Category</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase">Time</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase">Hours</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white">
              <tr v-for="visit in onSiteVisits" :key="visit.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">
                  {{ new Date(visit.activity_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) }}
                </td>
                <td class="px-4 py-3 text-sm font-medium text-gray-900">
                  {{ visit.customer_name || 'N/A' }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-600">
                  {{ visit.location || 'N/A' }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-600">
                  {{ visit.support_staff_name || 'N/A' }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    v-if="visit.task_category"
                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                    :style="{ backgroundColor: visit.task_category.color + '20', color: visit.task_category.color }"
                  >
                    {{ visit.task_category.title }}
                  </span>
                  <span v-else class="text-gray-400 text-xs">-</span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-600 text-center whitespace-nowrap">
                  {{ visit.start_time }} - {{ visit.end_time }}
                </td>
                <td class="px-4 py-3 text-sm font-semibold text-green-600 text-right">
                  {{ visit.duration_hours?.toFixed(1) || '0.0' }}h
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
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
          <p class="mt-2 text-sm text-gray-500">No on-site visits recorded yet</p>
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
import { useFieldActivities } from "@/composables/useFieldActivities";
import { LocationType } from "@/types/field";

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

// Computed property for top customers
const topCustomers = computed(() => {
  if (!analytics.value?.top_customers) return [];
  return analytics.value.top_customers.filter(c => c.customer_name !== "SAJSOFT SYSTEMS");
});

// Fetch recent on-site activities
const {
  data: activities,
  isLoading: activitiesLoading,
} = useFieldActivities(currentWorkspaceId);

// Filter and sort on-site visits
const onSiteVisits = computed(() => {
  if (!activities.value) return [];
  return activities.value
    .filter(activity => activity.location_type === LocationType.ON_SITE)
    .sort((a, b) => {
      // Sort by date descending (most recent first)
      const dateCompare = new Date(b.activity_date).getTime() - new Date(a.activity_date).getTime();
      if (dateCompare !== 0) return dateCompare;
      // If same date, sort by time (handle null values)
      if (!b.start_time || !a.start_time) return 0;
      return b.start_time.localeCompare(a.start_time);
    })
    .slice(0, 10); // Show only latest 10
});
</script>
