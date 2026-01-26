<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg
                class="h-6 w-6 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
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
                  Total Tasks
                </dt>
                <dd class="text-lg font-semibold text-gray-900">
                  {{ taskStore.myTasks.length }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg
                class="h-6 w-6 text-green-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Completed
                </dt>
                <dd class="text-lg font-semibold text-gray-900">
                  {{ completedTasks }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg
                class="h-6 w-6 text-blue-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  In Progress
                </dt>
                <dd class="text-lg font-semibold text-gray-900">
                  {{ inProgressTasks }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg
                class="h-6 w-6 text-red-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
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
                  Overdue
                </dt>
                <dd class="text-lg font-semibold text-gray-900">
                  {{ overdueTasks }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Tasks</h3>
        <div v-if="loading" class="text-center py-4">Loading...</div>
        <div
          v-else-if="taskStore.myTasks.length === 0"
          class="text-center py-8 text-gray-500"
        >
          No tasks assigned to you
        </div>
        <ul v-else class="divide-y divide-gray-200">
          <li v-for="task in recentTasks" :key="task.id" class="py-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <RouterLink
                  :to="`/task/${task.id}`"
                  class="text-sm font-medium text-primary-600 hover:text-primary-800"
                >
                  {{ task.title }}
                </RouterLink>
                <p class="text-xs text-gray-500 mt-1">{{ task.description }}</p>
                <p v-if="task.assignee_name" class="text-xs text-gray-600 mt-1">
                  <span class="font-medium">Assignee:</span>
                  {{
                    task.assignee_name.split(" ")[
                      task.assignee_name.split(" ").length - 1
                    ]
                  }}
                </p>
              </div>
              <div class="flex items-center space-x-2 ml-4">
                <span
                  :class="getStatusClass(task.status)"
                  class="px-2 py-1 text-xs font-medium rounded-full"
                >
                  {{ formatStatus(task.status) }}
                </span>
                <span
                  :class="getPriorityClass(task.priority)"
                  class="px-2 py-1 text-xs font-medium rounded-full"
                >
                  {{ task.priority }}
                </span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useTaskStore } from "@/stores/task";
import { TaskStatus } from "@/types/task";

const taskStore = useTaskStore();
const loading = ref(true);

const completedTasks = computed(
  () =>
    taskStore.myTasks.filter((t) => t.status === TaskStatus.COMPLETED).length,
);

const inProgressTasks = computed(
  () =>
    taskStore.myTasks.filter((t) => t.status === TaskStatus.IN_PROGRESS).length,
);

const overdueTasks = computed(() => {
  const now = new Date();
  return taskStore.myTasks.filter(
    (t) =>
      t.due_date &&
      new Date(t.due_date) < now &&
      t.status !== TaskStatus.COMPLETED,
  ).length;
});

const recentTasks = computed(() => taskStore.myTasks.slice(0, 10));

const getStatusClass = (status: TaskStatus) => {
  const classes = {
    [TaskStatus.TODO]: "bg-gray-100 text-gray-800",
    [TaskStatus.IN_PROGRESS]: "bg-blue-100 text-blue-800",
    [TaskStatus.IN_REVIEW]: "bg-purple-100 text-purple-800",
    [TaskStatus.COMPLETED]: "bg-green-100 text-green-800",
    [TaskStatus.BLOCKED]: "bg-red-100 text-red-800",
  };
  return classes[status];
};

const getPriorityClass = (priority: string) => {
  const classes = {
    low: "bg-gray-100 text-gray-600",
    medium: "bg-yellow-100 text-yellow-600",
    high: "bg-orange-100 text-orange-600",
    urgent: "bg-red-100 text-red-600",
  };
  return classes[priority as keyof typeof classes];
};

const formatStatus = (status: string) => {
  return status.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
};

onMounted(async () => {
  try {
    await taskStore.fetchMyTasks();
  } finally {
    loading.value = false;
  }
});
</script>
