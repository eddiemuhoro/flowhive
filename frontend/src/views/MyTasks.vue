<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">My Tasks</h1>

    <div class="mb-6 flex space-x-4">
      <button
        v-for="status in ['all', 'todo', 'in_progress', 'completed']"
        :key="status"
        @click="filterStatus = status"
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium',
          filterStatus === status
            ? 'bg-primary-600 text-white'
            : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
        ]"
      >
        {{ formatStatus(status) }}
      </button>
    </div>

    <div v-if="taskStore.loading" class="text-center py-12">Loading...</div>

    <div v-else class="bg-white shadow rounded-lg">
      <ul class="divide-y divide-gray-200">
        <li
          v-for="task in filteredTasks"
          :key="task.id"
          class="p-4 hover:bg-gray-50"
        >
          <RouterLink :to="`/task/${task.id}`" class="block">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <h3 class="text-sm font-medium text-gray-900">{{ task.title }}</h3>
                <p class="text-xs text-gray-500 mt-1">{{ task.description }}</p>
              </div>
              <div class="flex items-center space-x-2 ml-4">
                <span :class="getStatusClass(task.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ formatStatus(task.status) }}
                </span>
                <span :class="getPriorityClass(task.priority)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ task.priority }}
                </span>
              </div>
            </div>
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/task'
import { TaskStatus } from '@/types/task'

const taskStore = useTaskStore()
const filterStatus = ref('all')

const filteredTasks = computed(() => {
  if (filterStatus.value === 'all') {
    return taskStore.myTasks
  }
  return taskStore.myTasks.filter(t => t.status === filterStatus.value)
})

const getStatusClass = (status: TaskStatus) => {
  const classes = {
    [TaskStatus.TODO]: 'bg-gray-100 text-gray-800',
    [TaskStatus.IN_PROGRESS]: 'bg-blue-100 text-blue-800',
    [TaskStatus.IN_REVIEW]: 'bg-purple-100 text-purple-800',
    [TaskStatus.COMPLETED]: 'bg-green-100 text-green-800',
    [TaskStatus.BLOCKED]: 'bg-red-100 text-red-800'
  }
  return classes[status]
}

const getPriorityClass = (priority: string) => {
  const classes = {
    low: 'bg-gray-100 text-gray-600',
    medium: 'bg-yellow-100 text-yellow-600',
    high: 'bg-orange-100 text-orange-600',
    urgent: 'bg-red-100 text-red-600'
  }
  return classes[priority as keyof typeof classes]
}

const formatStatus = (status: string) => {
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

onMounted(() => {
  taskStore.fetchMyTasks()
})
</script>
