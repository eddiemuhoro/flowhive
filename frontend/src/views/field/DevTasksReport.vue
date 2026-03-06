<!-- Dev Tasks Report View -->
<!-- Simple view for field staff to see what devs are working on -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Dev Team Tasks</h1>
          <p class="mt-1 text-sm text-gray-600">
            What the development team is working on
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
            <span>Back to Activities</span>
          </button>
          <button
            @click="loadTasks"
            :disabled="isLoading"
            class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
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
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            <span>Refresh</span>
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="rounded-lg bg-white p-4 shadow-sm">
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Filter by Status
            </label>
            <select
              v-model="selectedStatus"
              @change="loadTasks"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            >
              <option value="">All Statuses</option>
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="in_review">In Review</option>
              <option value="completed">Completed</option>
              <option value="blocked">Blocked</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Filter by Person
            </label>
            <select
              v-model="selectedAssignee"
              @change="loadTasks"
              :disabled="isLoadingUsers"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none disabled:opacity-50"
            >
              <option :value="undefined">All People</option>
              <option
                v-for="user in users"
                :key="user.id"
                :value="user.id"
              >
                {{ user.full_name || user.username }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div
            class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
          <p class="mt-2 text-sm text-gray-600">Loading dev tasks...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="rounded-lg bg-red-50 p-4">
        <p class="text-sm text-red-700">{{ error }}</p>
      </div>

      <!-- Tasks Content -->
      <div v-else-if="tasks.length > 0">
        <!-- Summary Stats -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Summary</h2>
          <div class="grid grid-cols-2 gap-6 md:grid-cols-4">
            <div>
              <p class="text-sm text-gray-600">Total Tasks</p>
              <p class="mt-1 text-2xl font-bold text-gray-900">
                {{ summary.total }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">In Progress</p>
              <p class="mt-1 text-2xl font-bold text-blue-600">
                {{ summary.inProgress }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Completed</p>
              <p class="mt-1 text-2xl font-bold text-green-600">
                {{ summary.completed }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Blocked</p>
              <p class="mt-1 text-2xl font-bold text-red-600">
                {{ summary.blocked }}
              </p>
            </div>
          </div>
        </div>

        <!-- Tasks List -->
        <div class="space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Task List</h2>

          <div class="space-y-3">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="rounded-lg bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-base font-semibold text-gray-900">
                      {{ task.title }}
                    </h3>
                    <span
                      :class="getStatusClass(task.status)"
                      class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                    >
                      {{ formatStatus(task.status) }}
                    </span>
                    <span
                      v-if="task.priority"
                      :class="getPriorityClass(task.priority)"
                      class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                    >
                      {{ formatPriority(task.priority) }}
                    </span>
                  </div>

                  <p
                    v-if="task.description"
                    class="mt-2 text-sm text-gray-600 line-clamp-2"
                  >
                    {{ task.description }}
                  </p>

                  <div
                    class="mt-3 flex items-center space-x-4 text-sm text-gray-500"
                  >
                    <div
                      v-if="task.assignee_name || task.creator_name"
                      class="flex items-center space-x-1"
                    >
                      <svg
                        class="h-4 w-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                      <span>{{ task.assignee_name || task.creator_name }}</span>
                    </div>

                    <div
                      v-if="(task.status === 'completed' && task.updated_at) || ((task.status === 'todo' || task.status === 'in_progress') && task.due_date)"
                      class="flex items-center space-x-1"
                    >
                      <svg
                        class="h-4 w-4"
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
                      <span v-if="task.status === 'completed'">
                        {{ formatDate(task.updated_at) }}
                      </span>
                      <span v-else-if="(task.status === 'todo' || task.status === 'in_progress') && task.due_date" :class="isOverdue(task.due_date) ? 'text-red-600' : ''">
                        Due {{ formatDate(task.due_date) }}
                      </span>
                    </div>

                    <div
                      v-if="task.estimated_hours"
                      class="flex items-center space-x-1"
                    >
                      <svg
                        class="h-4 w-4"
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
                      <span>{{ task.estimated_hours }}h estimated</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

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
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
        <p class="mt-1 text-sm text-gray-500">
          The dev team has no tasks matching your filter criteria
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useDevTasks } from "@/composables/useDevTasks";
import { userService } from "@/services/user.service";
import type { User } from "@/types/auth";

const router = useRouter();
const { tasks, isLoading, error, fetchTasks, summary } = useDevTasks();

const selectedStatus = ref<string>("");
const selectedAssignee = ref<number | undefined>(undefined);
const users = ref<User[]>([]);
const isLoadingUsers = ref(false);

const loadUsers = async () => {
  isLoadingUsers.value = true;
  try {
    users.value = await userService.getAllUsers();
  } catch (err: any) {
    console.error("Error loading users:", err);
  } finally {
    isLoadingUsers.value = false;
  }
};

const loadTasks = async () => {
  await fetchTasks(
    undefined,
    selectedStatus.value || undefined,
    selectedAssignee.value
  );
};

// Status badge styling
const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    todo: "bg-gray-100 text-gray-800",
    in_progress: "bg-blue-100 text-blue-800",
    in_review: "bg-purple-100 text-purple-800",
    completed: "bg-green-100 text-green-800",
    blocked: "bg-red-100 text-red-800",
  };
  return classes[status] || "bg-gray-100 text-gray-800";
};

// Priority badge styling
const getPriorityClass = (priority: string) => {
  const classes: Record<string, string> = {
    low: "bg-gray-100 text-gray-600",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-orange-100 text-orange-800",
    urgent: "bg-red-100 text-red-800",
  };
  return classes[priority] || "bg-gray-100 text-gray-600";
};

// Format status for display
const formatStatus = (status: string) => {
  const formatted: Record<string, string> = {
    todo: "To Do",
    in_progress: "In Progress",
    in_review: "In Review",
    completed: "Completed",
    blocked: "Blocked",
  };
  return formatted[status] || status;
};

// Format priority for display
const formatPriority = (priority: string) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1);
};

// Format date
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

// Check if task is overdue
const isOverdue = (dueDate: string) => {
  return new Date(dueDate) < new Date();
};

onMounted(async () => {
  await loadUsers();
  await loadTasks();
});
</script>
