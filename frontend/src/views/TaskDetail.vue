<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Task Details</h1>
    <div v-if="taskStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="taskStore.currentTask" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-2xl font-semibold mb-4">{{ taskStore.currentTask.title }}</h2>
        <p class="text-gray-600 mb-4">{{ taskStore.currentTask.description }}</p>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <span class="text-sm font-medium text-gray-500">Status:</span>
            <span :class="getStatusClass(taskStore.currentTask.status)" class="ml-2 px-2 py-1 text-xs font-medium rounded-full">
              {{ formatStatus(taskStore.currentTask.status) }}
            </span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Priority:</span>
            <span :class="getPriorityClass(taskStore.currentTask.priority)" class="ml-2 px-2 py-1 text-xs font-medium rounded-full">
              {{ taskStore.currentTask.priority }}
            </span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Assignee:</span>
            <span class="ml-2 text-sm">{{ taskStore.currentTask.assignee_name || 'Unassigned' }}</span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Due Date:</span>
            <span class="ml-2 text-sm">{{ taskStore.currentTask.due_date ? new Date(taskStore.currentTask.due_date).toLocaleDateString() : 'Not set' }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold mb-4">Comments</h3>
        <div class="space-y-4">
          <div v-for="comment in taskStore.comments" :key="comment.id" class="border-l-2 border-gray-200 pl-4">
            <div class="flex items-center space-x-2 mb-1">
              <span class="text-sm font-medium">{{ comment.user_name }}</span>
              <span class="text-xs text-gray-500">{{ new Date(comment.created_at).toLocaleDateString() }}</span>
            </div>
            <p class="text-sm text-gray-700">{{ comment.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { TaskStatus } from '@/types/task'

const route = useRoute()
const taskStore = useTaskStore()

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

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await taskStore.fetchTask(id)
  await taskStore.fetchComments(id)
})
</script>
