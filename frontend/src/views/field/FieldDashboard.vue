<!-- Field Dashboard View -->
<!-- Main dashboard for field operations team members -->

<template>
  <div class="min-h-full bg-gray-50 pb-20 lg:pb-6">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <div
        class="bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-6 md:px-6 lg:rounded-b-lg"
      >
        <h1 class="text-2xl font-bold text-white md:text-3xl">
          Field Dashboard
        </h1>
        <p class="mt-1 text-blue-100">
          Welcome back, {{ currentUser?.full_name || currentUser?.username }}
        </p>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-6 md:p-6">
        <!-- Quick Stats -->
        <div class="grid grid-cols-2 gap-3 md:gap-4 lg:grid-cols-4">
          <!-- Today's Activities -->
          <div
            class="rounded-xl bg-white p-4 shadow-sm hover:shadow-md transition-shadow md:p-5"
          >
            <div class="flex items-center justify-between mb-2">
              <p class="text-xs font-medium text-gray-600 md:text-sm">Today</p>
              <div class="rounded-full bg-blue-100 p-2">
                <svg
                  class="h-4 w-4 text-blue-600 md:h-5 md:w-5"
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
            <p class="text-2xl font-bold text-gray-900 md:text-3xl">
              {{ todayCount }}
            </p>
            <p class="mt-1 text-xs text-gray-500">Activities</p>
          </div>

          <!-- This Week -->
          <div
            class="rounded-xl bg-white p-4 shadow-sm hover:shadow-md transition-shadow md:p-5"
          >
            <div class="flex items-center justify-between mb-2">
              <p class="text-xs font-medium text-gray-600 md:text-sm">
                This Week
              </p>
              <div class="rounded-full bg-green-100 p-2">
                <svg
                  class="h-4 w-4 text-green-600 md:h-5 md:w-5"
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
            </div>
            <p class="text-2xl font-bold text-gray-900 md:text-3xl">
              {{ weekCount }}
            </p>
            <p class="mt-1 text-xs text-gray-500">Activities</p>
          </div>

          <!-- Total Hours (This Week) -->
          <div
            class="rounded-xl bg-white p-4 shadow-sm hover:shadow-md transition-shadow md:p-5"
          >
            <div class="flex items-center justify-between mb-2">
              <p class="text-xs font-medium text-gray-600 md:text-sm">Hours</p>
              <div class="rounded-full bg-purple-100 p-2">
                <svg
                  class="h-4 w-4 text-purple-600 md:h-5 md:w-5"
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
            <p class="text-2xl font-bold text-gray-900 md:text-3xl">
              {{ weekHours.toFixed(1) }}
            </p>
            <p class="mt-1 text-xs text-gray-500">This week</p>
          </div>

          <!-- This Month -->
          <div
            class="rounded-xl bg-white p-4 shadow-sm hover:shadow-md transition-shadow md:p-5"
          >
            <div class="flex items-center justify-between mb-2">
              <p class="text-xs font-medium text-gray-600 md:text-sm">
                This Month
              </p>
              <div class="rounded-full bg-orange-100 p-2">
                <svg
                  class="h-4 w-4 text-orange-600 md:h-5 md:w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
            </div>
            <p class="text-2xl font-bold text-gray-900 md:text-3xl">
              {{ monthCount }}
            </p>
            <p class="mt-1 text-xs text-gray-500">Activities</p>
          </div>
        </div>
        <div class="rounded-lg bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">This Month</p>
              <p class="mt-2 text-3xl font-bold text-gray-900">
                {{ monthCount }}
              </p>
            </div>
            <div class="rounded-full bg-orange-100 p-3">
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
                  d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="rounded-xl bg-white p-5 shadow-sm md:p-6">
        <h2 class="text-lg font-semibold text-gray-900 md:text-xl">
          Quick Actions
        </h2>
        <div class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <button
            @click="showActivityForm = true"
            class="group flex items-center space-x-4 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 p-4 text-left transition-all hover:from-blue-600 hover:to-blue-700 hover:shadow-lg active:scale-95"
          >
            <div
              class="rounded-full bg-white bg-opacity-20 p-3 backdrop-blur-sm"
            >
              <svg
                class="h-6 w-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
            </div>
            <div class="flex-1">
              <p class="font-semibold text-white">Log New Activity</p>
              <p class="text-sm text-blue-100">Record your field work</p>
            </div>
            <svg
              class="h-5 w-5 text-white opacity-0 group-hover:opacity-100 transition-opacity"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>

          <router-link
            to="/field/activities"
            class="group flex items-center space-x-4 rounded-xl border-2 border-gray-200 bg-white p-4 transition-all hover:border-blue-500 hover:shadow-md active:scale-95"
          >
            <div
              class="rounded-full bg-gray-100 p-3 group-hover:bg-blue-100 transition-colors"
            >
              <svg
                class="h-6 w-6 text-gray-600 group-hover:text-blue-600 transition-colors"
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
            <div class="flex-1">
              <p class="font-semibold text-gray-900">View All Activities</p>
              <p class="text-sm text-gray-500">Browse activity history</p>
            </div>
            <svg
              class="h-5 w-5 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </router-link>

          <router-link
            v-if="canViewAnalytics"
            to="/field/analytics"
            class="group flex items-center space-x-4 rounded-xl border-2 border-gray-200 bg-white p-4 transition-all hover:border-purple-500 hover:shadow-md active:scale-95 sm:col-span-2"
          >
            <div
              class="rounded-full bg-purple-100 p-3 group-hover:bg-purple-200 transition-colors"
            >
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
            <div class="flex-1">
              <p class="font-semibold text-gray-900">View Analytics</p>
              <p class="text-sm text-gray-500">Team performance & insights</p>
            </div>
            <svg
              class="h-5 w-5 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Recent Activities -->
      <div class="rounded-lg bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Recent Activities</h2>
          <div class="flex items-center space-x-3">
            <!-- View Toggle -->
            <div class="inline-flex rounded-lg border border-gray-200 p-1">
              <button
                @click="viewMode = 'my'"
                :class="[
                  'rounded-md px-3 py-1.5 text-sm font-medium transition-all',
                  viewMode === 'my'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                My Work
              </button>
              <button
                @click="viewMode = 'team'"
                :class="[
                  'rounded-md px-3 py-1.5 text-sm font-medium transition-all',
                  viewMode === 'team'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                Team
              </button>
            </div>
            <router-link
              to="/field/activities"
              class="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              View All →
            </router-link>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div
            class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
        </div>

        <!-- Activities List -->
        <div v-else-if="recentActivities.length > 0" class="space-y-3">
          <ActivityCard
            v-for="activity in recentActivities"
            :key="activity.id"
            :activity="activity"
            :show-description="false"
            :show-actions="true"
            @view="viewActivity"
            @edit="editActivity"
            @delete="deleteActivity"
          />
        </div>

        <!-- Empty State -->
        <div v-else class="py-12 text-center">
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
          <p class="mt-2 text-sm text-gray-600">No activities logged yet</p>
          <button
            @click="showActivityForm = true"
            class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Log Your First Activity
          </button>
        </div>
      </div>
    </div>

    <!-- Activity Form Modal -->
    <Teleport to="body">
      <div
        v-if="showActivityForm"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeActivityForm"
      >
        <div class="mx-auto max-w-2xl rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">
              {{ editingActivity ? "Edit Activity" : "Log New Activity" }}
            </h2>
            <button
              @click="closeActivityForm"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100"
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <ActivityForm
            :workspace-id="currentWorkspaceId"
            :activity="editingActivity"
            :loading="formLoading"
            @submit="handleActivitySubmit"
            @cancel="closeActivityForm"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";
import { useFieldActivityStore } from "@/stores/fieldActivity";
import ActivityCard from "@/components/field/activity/ActivityCard.vue";
import ActivityForm from "@/components/field/activity/ActivityForm.vue";
import type { FieldActivityCreate, FieldActivityUpdate } from "@/types/field";

const router = useRouter();
const authStore = useAuthStore();
const workspaceStore = useWorkspaceStore();
const activityStore = useFieldActivityStore();

const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);

const canViewAnalytics = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  return role === "MANAGER" || role === "EXECUTIVE";
});

const loading = ref(false);
const formLoading = ref(false);
const showActivityForm = ref(false);
const editingActivity = ref<any>(null);
const viewMode = ref<'my' | 'team'>('team'); // Default to team view for collaboration

const recentActivities = computed(() => {
  return activityStore.sortedActivities.slice(0, 5);
});

// Stats calculations (always personal stats)
const todayCount = computed(() => {
  const today = new Date().toISOString().split("T")[0];
  return activityStore.activities.filter(
    (a) => a.activity_date === today && a.support_staff_id === currentUser.value?.id
  ).length;
});

const weekCount = computed(() => {
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  return activityStore.activities.filter((a) => {
    const date = new Date(a.activity_date);
    return date >= weekAgo && date <= now && a.support_staff_id === currentUser.value?.id;
  }).length;
});

const weekHours = computed(() => {
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  return activityStore.activities
    .filter((a) => {
      const date = new Date(a.activity_date);
      return date >= weekAgo && date <= now && a.support_staff_id === currentUser.value?.id;
    })
    .reduce((sum, a) => sum + a.duration_hours, 0);
});

const monthCount = computed(() => {
  const now = new Date();
  const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  return activityStore.activities.filter((a) => {
    const date = new Date(a.activity_date);
    return date >= monthAgo && date <= now && a.support_staff_id === currentUser.value?.id;
  }).length;
});

const loadActivities = async () => {
  if (!currentWorkspaceId.value) return;

  loading.value = true;
  try {
    // Load recent activities (last 7 days)
    const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
      .toISOString()
      .split("T")[0];
    await activityStore.fetchActivities(currentWorkspaceId.value, {
      date_from: sevenDaysAgo,
      support_staff_id: viewMode.value === 'my' ? currentUser.value?.id : undefined,
    });
  } catch (error) {
    console.error("Failed to load activities:", error);
  } finally {
    loading.value = false;
  }
};

const viewActivity = (activityId: number) => {
  router.push(`/field/activities/${activityId}`);
};

const editActivity = async (activityId: number) => {
  const activity = activityStore.activities.find((a) => a.id === activityId);
  if (activity) {
    editingActivity.value = activity;
    showActivityForm.value = true;
  }
};

const deleteActivity = async (activityId: number) => {
  if (!confirm("Are you sure you want to delete this activity?")) return;

  try {
    await activityStore.deleteActivity(activityId, currentWorkspaceId.value);
  } catch (error) {
    console.error("Failed to delete activity:", error);
    alert("Failed to delete activity. Please try again.");
  }
};

const handleActivitySubmit = async (
  data: FieldActivityCreate | FieldActivityUpdate,
) => {
  formLoading.value = true;
  try {
    if (editingActivity.value) {
      await activityStore.updateActivity(
        editingActivity.value.id,
        currentWorkspaceId.value,
        data as FieldActivityUpdate,
      );
    } else {
      await activityStore.createActivity(data as FieldActivityCreate);
    }
    closeActivityForm();
    await loadActivities();
  } catch (error: any) {
    console.error("Failed to save activity:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to save activity. Please try again.",
    );
  } finally {
    formLoading.value = false;
  }
};

const closeActivityForm = () => {
  showActivityForm.value = false;
  editingActivity.value = null;
};

// Watch for view mode changes and reload activities
watch(viewMode, () => {
  loadActivities();
});

onMounted(() => {
  loadActivities();
});
</script>
