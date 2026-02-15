<!-- Pending Tasks Page -->
<!-- Dedicated page for managing pending task assignments -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Pending Tasks</h1>
          <p class="mt-1 text-sm text-gray-600">
            {{ isManagerOrExecutive ? 'Manage and track pending tasks' : 'Tasks assigned to you that need completion' }}
          </p>
        </div>

        <!-- Action Buttons for Managers/Executives -->
        <div v-if="isManagerOrExecutive" class="flex space-x-3">
          <button
            @click="openAssignTaskModal"
            class="flex items-center space-x-2 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Assign Task</span>
          </button>
          <button
            @click="openLogActivityModal"
            class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Log Activity</span>
          </button>
        </div>
        <!-- Action Button for Field Staff -->
        <button
          v-else
          @click="openLogActivityModal"
          class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Log Activity</span>
        </button>
      </div>

      <!-- Tasks Assigned By Me (Managers/Executives Only) -->
      <div v-if="isManagerOrExecutive" class="rounded-lg bg-white p-6 shadow">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Tasks I Assigned</h2>
            <p class="mt-1 text-sm text-gray-600">
              {{ assignedByMe.length }} task{{ assignedByMe.length !== 1 ? 's' : '' }} awaiting completion
            </p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loadingAssignedByMe" class="py-8 text-center">
          <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
          <p class="mt-2 text-sm text-gray-600">Loading assigned tasks...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="assignedByMe.length === 0" class="py-8 text-center">
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
          <p class="mt-2 text-sm text-gray-600">No tasks assigned to staff</p>
          <button
            @click="openAssignTaskModal"
            class="mt-4 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700"
          >
            Assign First Task
          </button>
        </div>

        <!-- Tasks List -->
        <div v-else class="space-y-3">
          <div
            v-for="task in assignedByMe"
            :key="task.id"
            class="cursor-pointer rounded-lg border border-gray-200 p-4 transition hover:border-blue-500 hover:bg-blue-50"
            @click="viewTaskDetails(task)"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-medium text-gray-900">{{ task.title }}</h3>
                <div class="mt-2 space-y-1 text-sm text-gray-600">
                  <div class="flex items-center">
                    <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    <span>Assigned to: <strong>{{ task.support_staff_name }}</strong></span>
                  </div>
                  <div class="flex items-center">
                    <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <span>{{ formatDate(task.activity_date) }}</span>
                  </div>
                  <div class="flex items-center">
                    <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                    <span>{{ task.customer_name }} - {{ task.location }}</span>
                  </div>
                  <div v-if="task.task_category" class="flex items-center">
                    <span
                      class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium"
                      :style="{ backgroundColor: task.task_category.color + '20', color: task.task_category.color }"
                    >
                      {{ task.task_category.title }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="ml-4">
                <span class="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800">
                  Pending
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tasks Assigned To Me -->

        <PendingTasks
          :pending-tasks="pendingTasks"
          :loading="loadingPending"
          @complete="handleCompleteTask"
        />

      <!-- Back to Dashboard -->
      <div class="text-center">
        <router-link
          to="/field"
          class="inline-flex items-center text-sm text-blue-600 hover:text-blue-700"
        >
          <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Task Form Modal -->
    <Teleport to="body">
      <div
        v-if="showTaskModal"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeTaskModal"
      >
        <div class="mx-auto max-w-2xl rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">
              {{ modalTitle }}
            </h2>
            <button
              @click="closeTaskModal"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <ActivityForm
            :workspace-id="currentWorkspaceId"
            :activity="selectedTask"
            :mode="formMode"
            :loading="isSubmitting"
            @submit="handleTaskSubmit"
            @cancel="closeTaskModal"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useWorkspaceStore } from '@/stores/workspace';
import { fieldActivityService } from '@/services/fieldActivity.service';
import PendingTasks from '@/components/field/activity/PendingTasks.vue';
import ActivityForm from '@/components/field/activity/ActivityForm.vue';
import type { FieldActivity, FieldActivityCreate, FieldActivityUpdate } from '@/types/field';
const authStore = useAuthStore();
const workspaceStore = useWorkspaceStore();

const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);

const isManagerOrExecutive = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  return role === 'MANAGER' || role === 'EXECUTIVE';
});

const pendingTasks = ref<FieldActivity[]>([]);
const assignedByMe = ref<FieldActivity[]>([]);
const loadingPending = ref(false);
const loadingAssignedByMe = ref(false);
const showTaskModal = ref(false);
const formMode = ref<'create' | 'assign' | 'complete'>('create');
const selectedTask = ref<FieldActivity | undefined>();
const isSubmitting = ref(false);

const modalTitle = computed(() => {
  if (formMode.value === 'assign') return 'Assign Task to Staff';
  if (formMode.value === 'complete') return 'Complete Task';
  return 'Log Activity';
});

const loadPendingTasks = async () => {
  if (!currentWorkspaceId.value) return;

  try {
    loadingPending.value = true;
    pendingTasks.value = await fieldActivityService.getPendingTasks(currentWorkspaceId.value);
  } catch (error) {
    console.error('Failed to load pending tasks:', error);
  } finally {
    loadingPending.value = false;
  }
};

const loadAssignedByMe = async () => {
  if (!currentWorkspaceId.value || !isManagerOrExecutive.value) return;

  try {
    loadingAssignedByMe.value = true;
    assignedByMe.value = await fieldActivityService.getTasksAssignedByMe(currentWorkspaceId.value);
  } catch (error) {
    console.error('Failed to load assigned tasks:', error);
  } finally {
    loadingAssignedByMe.value = false;
  }
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const viewTaskDetails = (task: FieldActivity) => {
  // For now, just show an alert. You could navigate to a detail view or open a modal
  alert(`Task: ${task.title}\nAssigned to: ${task.support_staff_name}\nCustomer: ${task.customer_name}\nLocation: ${task.location}`);
};

const openAssignTaskModal = () => {
  formMode.value = 'assign';
  selectedTask.value = undefined;
  showTaskModal.value = true;
};

const openLogActivityModal = () => {
  formMode.value = 'create';
  selectedTask.value = undefined;
  showTaskModal.value = true;
};

const handleCompleteTask = (task: FieldActivity) => {
  formMode.value = 'complete';
  selectedTask.value = task;
  showTaskModal.value = true;
};

const handleTaskSubmit = async (data: FieldActivityCreate | FieldActivityUpdate) => {
  try {
    isSubmitting.value = true;

    if (formMode.value === 'complete' && selectedTask.value) {
      // Update existing task
      await fieldActivityService.updateActivity(
        selectedTask.value.id,
        currentWorkspaceId.value,
        data as FieldActivityUpdate
      );
    } else {
      // Create new task or assigned task
      await fieldActivityService.createActivity(data as FieldActivityCreate);
    }

    // Reload pending tasks
    await loadPendingTasks();
    if (isManagerOrExecutive.value) {
      await loadAssignedByMe();
    }
    closeTaskModal();
  } catch (error: any) {
    console.error('Failed to submit task:', error);
    alert(error.response?.data?.detail || 'Failed to save task. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};

const closeTaskModal = () => {
  showTaskModal.value = false;
  selectedTask.value = undefined;
};

onMounted(() => {
  loadPendingTasks();
  if (isManagerOrExecutive.value) {
    loadAssignedByMe();
  }
});
</script>
